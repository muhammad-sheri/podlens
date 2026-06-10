"""ClickHouse access layer.

Analytics events live in ClickHouse (not the Django ORM). This module owns the
connection and schema so the rest of the app never talks to ClickHouse directly.
"""
import clickhouse_connect
from django.conf import settings

EVENTS_TABLE = "episode_events"


def get_client():
    """Return a ClickHouse client built from Django settings."""
    cfg = settings.CLICKHOUSE
    return clickhouse_connect.get_client(
        host=cfg["host"],
        port=cfg["port"],
        username=cfg["username"],
        password=cfg["password"],
        database=cfg["database"],
    )


def ensure_schema(client=None):
    """Create the analytics events table if it does not yet exist."""
    client = client or get_client()
    client.command(
        f"""
        CREATE TABLE IF NOT EXISTS {EVENTS_TABLE} (
            event_date     Date,
            podcast_id     UInt64,
            episode_id     UInt64,
            platform       LowCardinality(String),
            downloads      UInt32,
            listeners      UInt32,
            avg_retention  Float32
        )
        ENGINE = MergeTree()
        ORDER BY (podcast_id, episode_id, event_date, platform)
        """
    )
    return client
