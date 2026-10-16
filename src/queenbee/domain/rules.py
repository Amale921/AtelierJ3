"""Règles de détection (J1) : Strategy + Composite + Factory."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from queenbee.domain.model import Alert, DomainError, SecurityEvent, Severity


class Rule(Protocol):
    def evaluate(self, events: Sequence[SecurityEvent]) -> list[Alert]: ...


def _check_threshold(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise DomainError("threshold must be a positive integer")
    return value


class _CountingRule:
    name = ""
    action = ""
    severity = Severity.LOW
    default_threshold = 1

    def __init__(self, threshold: int | None = None) -> None:
        self.threshold = _check_threshold(
            self.default_threshold if threshold is None else threshold
        )

    def evaluate(self, events: Sequence[SecurityEvent]) -> list[Alert]:
        counts = Counter(e.source_ip for e in events if e.action == self.action)
        return [
            Alert(self.name, ip, self.severity, f"{n} x {self.action}")
            for ip, n in counts.items()
            if n >= self.threshold
        ]


class BruteForceRule(_CountingRule):
    name, action, severity, default_threshold = "brute_force", "login_failed", Severity.HIGH, 5


class PortScanRule(_CountingRule):
    name, action, severity, default_threshold = "port_scan", "port_probe", Severity.MEDIUM, 20


class RuleSet:
    def __init__(self, rules: Sequence[Rule]) -> None:
        self._rules = tuple(rules)

    def evaluate(self, events: Sequence[SecurityEvent]) -> list[Alert]:
        return [a for rule in self._rules for a in rule.evaluate(events)]


_REGISTRY: dict[str, type[_CountingRule]] = {
    "brute_force": BruteForceRule,
    "port_scan": PortScanRule,
}


def build_rule(spec: Mapping[str, Any]) -> Rule:
    kind = spec.get("kind")
    if not isinstance(kind, str) or kind not in _REGISTRY:
        raise DomainError("unknown rule kind")
    return _REGISTRY[kind](spec.get("threshold"))
