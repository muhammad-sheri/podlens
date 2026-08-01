"""Aggregation queries over the ClickHouse events table.

Every query is scoped to a set of podcast ids, which the view layer resolves.
PodLens is single-tenant, so that set is normally every podcast in Postgres.
"""
from .clickhouse import EVENTS_TABLE, get_client


def _podcast_filter(podcast_ids):
    """Return (sql_fragment, params) restricting to the given podcast ids."""
    if not podcast_ids:
        # No podcasts -> match nothing.
        return "0", {}
    return "podcast_id IN %(podcast_ids)s", {"podcast_ids": tuple(podcast_ids)}


def overview(podcast_ids, days=90):
    """Totals plus a daily downloads/listeners time series."""
    where, params = _podcast_filter(podcast_ids)
    client = get_client()

    totals = client.query(
        f"""
        SELECT
            sum(downloads)      AS downloads,
            sum(listeners)      AS listeners,
            round(avg(avg_retention), 1) AS avg_retention
        FROM {EVENTS_TABLE}
        WHERE {where} AND event_date >= today() - {int(days)}
        """,
        parameters=params,
    ).first_row or [0, 0, 0]

    series_rows = client.query(
        f"""
        SELECT
            event_date AS date,
            sum(downloads) AS downloads,
            sum(listeners) AS listeners
        FROM {EVENTS_TABLE}
        WHERE {where} AND event_date >= today() - {int(days)}
        GROUP BY event_date
        ORDER BY event_date
        """,
        parameters=params,
    ).result_rows

    return {
        "totals": {
            "downloads": int(totals[0] or 0),
            "listeners": int(totals[1] or 0),
            "avg_retention": float(totals[2] or 0),
        },
        "series": [
            {"date": str(d), "downloads": int(dl), "listeners": int(ls)}
            for d, dl, ls in series_rows
        ],
    }


def by_platform(podcast_ids, days=90):
    where, params = _podcast_filter(podcast_ids)
    rows = get_client().query(
        f"""
        SELECT platform, sum(downloads) AS downloads, sum(listeners) AS listeners
        FROM {EVENTS_TABLE}
        WHERE {where} AND event_date >= today() - {int(days)}
        GROUP BY platform
        ORDER BY downloads DESC
        """,
        parameters=params,
    ).result_rows
    return [
        {"platform": p, "downloads": int(dl), "listeners": int(ls)}
        for p, dl, ls in rows
    ]


def by_episode(podcast_ids, days=90):
    where, params = _podcast_filter(podcast_ids)
    rows = get_client().query(
        f"""
        SELECT
            episode_id,
            sum(downloads) AS downloads,
            sum(listeners) AS listeners,
            round(avg(avg_retention), 1) AS avg_retention
        FROM {EVENTS_TABLE}
        WHERE {where} AND event_date >= today() - {int(days)}
        GROUP BY episode_id
        ORDER BY downloads DESC
        """,
        parameters=params,
    ).result_rows
    return [
        {
            "episode_id": int(eid),
            "downloads": int(dl),
            "listeners": int(ls),
            "avg_retention": float(ret or 0),
        }
        for eid, dl, ls, ret in rows
    ]
