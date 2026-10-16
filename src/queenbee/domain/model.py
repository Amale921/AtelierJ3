"""Domaine (J1) : objets immuables, validés à la construction. Aucun import technique."""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from uuid import UUID, uuid4


class DomainError(Exception):
    """Violation d'une règle métier ou d'une validation du domaine."""


class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


ALLOWED_ACTIONS = frozenset({"login_failed", "login_ok", "port_probe"})
_USER_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")


@dataclass(frozen=True)
class SecurityEvent:
    source_ip: str
    user: str
    action: str
    timestamp: datetime

    def __post_init__(self) -> None:
        try:
            ipaddress.ip_address(self.source_ip)
        except ValueError as exc:
            raise DomainError("invalid source ip") from exc
        if not isinstance(self.user, str) or not _USER_RE.fullmatch(self.user):
            raise DomainError("invalid user")
        if self.action not in ALLOWED_ACTIONS:
            raise DomainError("action not allowed")
        if not isinstance(self.timestamp, datetime) or self.timestamp.tzinfo is None:
            raise DomainError("timestamp must be timezone-aware")


@dataclass(frozen=True)
class Alert:
    rule: str
    source_ip: str
    severity: Severity
    detail: str


class IncidentStatus(Enum):
    OPEN = "open"
    TRIAGED = "triaged"
    CLOSED = "closed"


_ALLOWED_TRANSITIONS: dict[IncidentStatus, frozenset[IncidentStatus]] = {
    IncidentStatus.OPEN: frozenset({IncidentStatus.TRIAGED}),
    IncidentStatus.TRIAGED: frozenset({IncidentStatus.CLOSED}),
    IncidentStatus.CLOSED: frozenset(),
}


@dataclass
class Incident:
    alert: Alert
    id: UUID = field(default_factory=uuid4)
    status: IncidentStatus = IncidentStatus.OPEN

    def transition_to(self, target: IncidentStatus) -> None:
        if target not in _ALLOWED_TRANSITIONS[self.status]:
            raise DomainError(f"transition {self.status.value} -> {target.value} forbidden")
        self.status = target


@dataclass(frozen=True)
class Principal:
    name: str
    roles: frozenset[str]
