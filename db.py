"""Datenbankzugriff für die Bestenliste (SQLite)."""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("ZAHLEN_RATEN_DB", os.path.join(BASE_DIR, "highscores.db"))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


@contextmanager
def _connect():
    """Öffnet eine Verbindung, schreibt Änderungen fest und schließt sie wieder."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db():
    """Legt die Tabelle an, falls sie noch nicht existiert."""
    with open(SCHEMA_PATH, encoding="utf-8") as schema, _connect() as connection:
        connection.executescript(schema.read())


def get_highscores(limit=10):
    """Liefert die besten Einträge: wenigste Versuche zuerst, bei Gleichstand der frühere."""
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, versuche, zeitpunkt FROM highscore "
            "ORDER BY versuche ASC, id ASC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_rank(score_id):
    """Platz eines Eintrags in der gesamten Bestenliste (auch außerhalb der Top 10)."""
    with _connect() as connection:
        row = connection.execute(
            "SELECT COUNT(*) + 1 AS platz FROM highscore AS other, highscore AS own "
            "WHERE own.id = ? AND (other.versuche < own.versuche "
            "OR (other.versuche = own.versuche AND other.id < own.id))",
            (score_id,),
        ).fetchone()
    return row["platz"]


def save_score(name, versuche):
    """Speichert ein Spielergebnis und gibt die neue ID zurück."""
    zeitpunkt = datetime.now().strftime("%d.%m.%Y %H:%M")
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO highscore (name, versuche, zeitpunkt) VALUES (?, ?, ?)",
            (name, versuche, zeitpunkt),
        )
        return cursor.lastrowid
