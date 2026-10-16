"""Adaptateurs d'entrée : tout ce qui vient de l'extérieur est hostile jusqu'à preuve du contraire.

- SignedEventReader : message borné, signé (HMAC-SHA256), schéma strict.
- LogLineAdapter    : ligne de journal -> SecurityEvent (Adapter), bornée, regex stricte.
Un rejet est toujours compté (attribut `rejected`).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from datetime import datetime
from typing import Any

from queenbee.domain.model import DomainError, SecurityEvent

MAX_MESSAGE_BYTES = 4096
MAX_LINE_CHARS = 256
_EVENT_KEYS = frozenset({"source_ip", "user", "action", "timestamp"})


class MessageRejected(Exception):
    """Entrée refusée (taille, signature, schéma ou validation du domaine)."""


def canonical(event: dict[str, str]) -> bytes:
    return json.dumps(event, sort_keys=True, separators=(",", ":")).encode()


def sign_event(key: bytes, event: dict[str, str]) -> bytes:
    """Côté agent : produit le message à envoyer."""
    sig = hmac.new(key, canonical(event), hashlib.sha256).hexdigest()
    return json.dumps({"event": event, "sig": sig}).encode()


class SignedEventReader:
    def __init__(self, key: bytes) -> None:
        if len(key) < 16:
            raise ValueError("signing key too short")
        self._key = key
        self.rejected = 0

    def parse(self, raw: bytes) -> SecurityEvent:
        try:
            return self._parse(raw)
        except MessageRejected:
            self.rejected += 1
            raise

    def _parse(self, raw: bytes) -> SecurityEvent:
        if not isinstance(raw, bytes | bytearray) or len(raw) > MAX_MESSAGE_BYTES:
            raise MessageRejected("size")
        try:
            msg: Any = json.loads(raw)
        except (ValueError, RecursionError) as exc:
            raise MessageRejected("json") from exc
        if not isinstance(msg, dict) or set(msg) != {"event", "sig"}:
            raise MessageRejected("schema")
        event, sig = msg["event"], msg["sig"]
        if not isinstance(sig, str) or not isinstance(event, dict):
            raise MessageRejected("schema")
        if set(event) != _EVENT_KEYS or not all(isinstance(v, str) for v in event.values()):
            raise MessageRejected("schema")
        expected = hmac.new(self._key, canonical(event), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected.encode(), sig.encode()):
            raise MessageRejected("signature")
        try:
            return SecurityEvent(
                event["source_ip"],
                event["user"],
                event["action"],
                datetime.fromisoformat(event["timestamp"]),
            )
        except (ValueError, DomainError) as exc:
            raise MessageRejected("domain") from exc


_LINE = re.compile(
    r"(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})) "
    r"(?P<action>[a-z_]{1,32}) user=(?P<user>[A-Za-z0-9_.-]{1,64}) ip=(?P<ip>[0-9a-fA-F:.]{2,45})"
)


class LogLineAdapter:
    def __init__(self) -> None:
        self.rejected = 0

    def parse(self, line: str) -> SecurityEvent:
        try:
            if not isinstance(line, str) or len(line) > MAX_LINE_CHARS:
                raise MessageRejected("size")
            m = _LINE.fullmatch(line)
            if m is None:
                raise MessageRejected("format")
            try:
                return SecurityEvent(
                    m["ip"], m["user"], m["action"], datetime.fromisoformat(m["ts"])
                )
            except (ValueError, DomainError) as exc:
                raise MessageRejected("domain") from exc
        except MessageRejected:
            self.rejected += 1
            raise
