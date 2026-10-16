"""A3 — entrées malveillantes : chaque test vérifie le refus ET l'absence d'effet de bord."""

import json
import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from queenbee.adapters.inbound.messages import (
    MAX_MESSAGE_BYTES,
    LogLineAdapter,
    MessageRejected,
    SignedEventReader,
    sign_event,
)
from queenbee.domain.model import SecurityEvent

KEY = b"0123456789abcdef-test-key"
GOOD = {
    "source_ip": "10.0.0.66",
    "user": "root",
    "action": "login_failed",
    "timestamp": "2026-10-14T09:00:00+00:00",
}


@pytest.fixture
def reader() -> SignedEventReader:
    return SignedEventReader(KEY)


def test_valid_signed_message_accepted(reader: SignedEventReader) -> None:
    event = reader.parse(sign_event(KEY, GOOD))
    assert event.source_ip == "10.0.0.66"
    assert reader.rejected == 0


def test_forged_signature_rejected(reader: SignedEventReader) -> None:
    forged = sign_event(b"another-attacker-key!!", GOOD)
    with pytest.raises(MessageRejected):
        reader.parse(forged)
    assert reader.rejected == 1


def test_tampered_field_after_signing_rejected(reader: SignedEventReader) -> None:
    msg = json.loads(sign_event(KEY, GOOD))
    msg["event"]["source_ip"] = "10.0.0.1"  # on change l'IP, la signature ne suit plus
    with pytest.raises(MessageRejected):
        reader.parse(json.dumps(msg).encode())
    assert reader.rejected == 1


def test_extra_field_rejected_even_if_signed(reader: SignedEventReader) -> None:
    event = {**GOOD, "is_admin": "true"}
    with pytest.raises(MessageRejected):
        reader.parse(sign_event(KEY, event))
    assert reader.rejected == 1


def test_oversized_message_rejected_before_parsing(reader: SignedEventReader) -> None:
    with pytest.raises(MessageRejected):
        reader.parse(b"{" + b" " * MAX_MESSAGE_BYTES + b"}")
    assert reader.rejected == 1


@pytest.mark.parametrize("raw", [b"not json", b"[]", b'{"event": 1, "sig": 2}', b"\xff\xfe"])
def test_garbage_rejected_and_counted(reader: SignedEventReader, raw: bytes) -> None:
    with pytest.raises(MessageRejected):
        reader.parse(raw)
    assert reader.rejected == 1


def test_signed_but_poisoned_user_rejected_by_domain(reader: SignedEventReader) -> None:
    event = {**GOOD, "user": "root'; DROP TABLE incidents;--"}
    with pytest.raises(MessageRejected):
        reader.parse(sign_event(KEY, event))


@pytest.mark.parametrize(
    "line",
    [
        "A" * 100_000,  # ligne énorme
        "2026-10-14T09:00:00Z login_failed user=root ip=10.0.0.1\nINJECTED fake line",
        "2026-10-14T09:00:00Z login_failed user=ro ot ip=10.0.0.1",
        "2026-10-14T09:00:00Z rm_rf user=root ip=10.0.0.1",
        "2026-10-14T09:00:00Z login_failed user=root ip=999.1.1.1",
        "2026-10-14T09:00:00 login_failed user=root ip=10.0.0.1",  # sans fuseau
    ],
)
def test_trapped_log_line_rejected_and_counted(line: str) -> None:
    adapter = LogLineAdapter()
    with pytest.raises(MessageRejected):
        adapter.parse(line)
    assert adapter.rejected == 1


def test_valid_log_line_accepted() -> None:
    event = LogLineAdapter().parse("2026-10-14T09:00:00Z login_failed user=root ip=10.0.0.66")
    assert event.action == "login_failed"


@given(st.binary(max_size=6000))
def test_hypothesis_random_bytes_never_crash_the_reader(raw: bytes) -> None:
    reader = SignedEventReader(KEY)
    try:
        assert isinstance(reader.parse(raw), SecurityEvent)
    except MessageRejected:
        assert reader.rejected == 1  # seule exception autorisée, et elle est comptée


_text = st.text(alphabet=string.printable + "é\u202e\x00", max_size=80)


@given(_text, _text, _text, _text)
def test_hypothesis_signed_garbage_fields_are_rejected_or_valid(
    ip: str, user: str, action: str, ts: str
) -> None:
    """Même avec une signature valide, le domaine doit refuser les champs hostiles."""
    reader = SignedEventReader(KEY)
    raw = sign_event(KEY, {"source_ip": ip, "user": user, "action": action, "timestamp": ts})
    try:
        event = reader.parse(raw)
        assert event.timestamp.tzinfo is not None
    except MessageRejected:
        assert reader.rejected == 1


@given(st.text(max_size=400))
def test_hypothesis_random_lines_never_crash_the_adapter(line: str) -> None:
    adapter = LogLineAdapter()
    try:
        adapter.parse(line)
    except MessageRejected:
        assert adapter.rejected == 1
