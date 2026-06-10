"""Prefect flow scaffolding.

Phase 1 wraps the mock-data seed in a Prefect flow so the orchestration pattern
is in place. Real platform ingestion (Spotify / YouTube / Apple) will later plug
in as additional tasks feeding the same ClickHouse events table.

Run with:  python pipeline/flows.py
"""
from prefect import flow, task


@task
def generate_analytics(days: int = 90):
    from pipeline.seed import seed

    seed(days=days)


@flow(name="refresh_analytics")
def refresh_analytics(days: int = 90):
    """Refresh the analytics store. Today: regenerate mock data."""
    generate_analytics(days)


if __name__ == "__main__":
    from pipeline.seed import _bootstrap_django

    _bootstrap_django()
    refresh_analytics()
