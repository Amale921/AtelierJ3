"""Racine de composition : seul endroit qui connaît tous les adaptateurs."""

from __future__ import annotations

import os
import sqlite3

from queenbee.adapters.inbound.messages import SignedEventReader
from queenbee.adapters.outbound.repositories import SqliteIncidentRepository
from queenbee.application.services import IncidentService


def build(db_path: str = "queenbee.db") -> tuple[SignedEventReader, IncidentService]:
    key = os.environ["QUEENBEE_AGENT_KEY"].encode()  # chargé depuis .env, jamais commité
    repo = SqliteIncidentRepository(sqlite3.connect(db_path))
    return SignedEventReader(key), IncidentService(repo)
