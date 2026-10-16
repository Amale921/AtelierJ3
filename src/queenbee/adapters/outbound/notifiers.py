"""Décorateurs et Observateur : même interface Notifier que l'objet enveloppé."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Sequence

from queenbee.application.ports import Notifier
from queenbee.domain.model import Alert

_audit = logging.getLogger("queenbee.audit")
_log = logging.getLogger(__name__)


class RateLimitedNotifier:
    """Fenêtre fixe : au plus max_per_window alertes par fenêtre, le reste est compté."""

    def __init__(
        self,
        inner: Notifier,
        max_per_window: int,
        window_s: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._inner, self._max, self._window, self._clock = inner, max_per_window, window_s, clock
        self._window_start = clock()
        self._sent = 0
        self.dropped = 0

    def notify(self, alert: Alert) -> None:
        now = self._clock()
        if now - self._window_start >= self._window:
            self._window_start, self._sent = now, 0
        if self._sent >= self._max:
            self.dropped += 1
            return
        self._sent += 1
        self._inner.notify(alert)


class AuditedNotifier:
    def __init__(self, inner: Notifier) -> None:
        self._inner = inner

    def notify(self, alert: Alert) -> None:
        _audit.info("alert rule=%s ip=%s severity=%s", alert.rule, alert.source_ip, alert.severity)
        self._inner.notify(alert)


class FanOutNotifier:
    """Observateur : un abonné en panne ne bloque pas les autres, la panne est comptée."""

    def __init__(self, subscribers: Sequence[Notifier]) -> None:
        self._subscribers = tuple(subscribers)
        self.failures = 0

    def notify(self, alert: Alert) -> None:
        for subscriber in self._subscribers:
            try:
                subscriber.notify(alert)
            except Exception:
                self.failures += 1
                _log.exception("subscriber failed")
