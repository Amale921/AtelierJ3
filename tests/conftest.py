from datetime import UTC, datetime

import pytest

from queenbee.domain.model import SecurityEvent

T0 = datetime(2026, 10, 14, 9, 0, tzinfo=UTC)


def ev(
    ip: str = "10.0.0.66", user: str = "root", action: str = "login_failed"
) -> SecurityEvent:
    return SecurityEvent(ip, user, action, T0)


@pytest.fixture
def five_failures() -> list[SecurityEvent]:
    return [ev() for _ in range(5)]


from hypothesis import settings  # noqa: E402

# Suite < 2 s : Hypothesis borné. Pour une chasse plus profonde : --hypothesis-profile=deep
settings.register_profile("fast", max_examples=40, deadline=None)
settings.register_profile("deep", max_examples=2_000, deadline=None)
settings.load_profile("fast")
