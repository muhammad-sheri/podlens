"""Seed demo data so the whole app runs and every chart renders locally.

Creates a demo user + podcasts + episodes in Postgres, then generates ~90 days
of realistic randomized analytics events in ClickHouse. Idempotent-ish: it wipes
the demo user's prior data before reseeding so repeated runs stay clean.

Runnable two ways:
    python manage.py seed_demo
    python pipeline/seed.py        (bootstraps Django itself)
"""
import datetime as dt
import random

DEMO_EMAIL = "demo@podlens.app"
DEMO_PASSWORD = "podlens-demo"

PODCASTS = [
    {
        "title": "The Indie Maker Show",
        "description": "Conversations with bootstrapped founders.",
        "platforms": "spotify,youtube,apple",
        "episodes": [
            "Shipping your first SaaS",
            "Pricing for early traction",
            "Cold outreach that works",
            "Bootstrapping vs raising",
            "Building in public",
        ],
    },
    {
        "title": "Audio First",
        "description": "The craft and business of podcasting.",
        "platforms": "spotify,apple",
        "episodes": [
            "Mic technique 101",
            "Editing on a budget",
            "Growing past 1k downloads",
            "Sponsorships explained",
        ],
    },
]

PLATFORM_WEIGHTS = {"spotify": 1.0, "youtube": 0.7, "apple": 0.5}


def seed(days: int = 90, log=print):
    """Create demo data. `log` lets the management command route output."""
    from django.contrib.auth import get_user_model

    from analytics.clickhouse import EVENTS_TABLE, ensure_schema
    from podcasts.models import Episode, Podcast

    User = get_user_model()

    user, created = User.objects.get_or_create(
        email=DEMO_EMAIL, defaults={"first_name": "Demo", "last_name": "Creator"}
    )
    user.set_password(DEMO_PASSWORD)
    user.save()
    log(f"{'Created' if created else 'Found'} demo user: {DEMO_EMAIL}")

    # Reset prior demo podcasts (cascades to episodes).
    Podcast.objects.filter(owner=user).delete()

    today = dt.date.today()
    rows = []
    for pod_spec in PODCASTS:
        podcast = Podcast.objects.create(
            owner=user,
            title=pod_spec["title"],
            description=pod_spec["description"],
            platforms=pod_spec["platforms"],
        )
        platforms = pod_spec["platforms"].split(",")
        for i, ep_title in enumerate(pod_spec["episodes"]):
            published = today - dt.timedelta(days=(len(pod_spec["episodes"]) - i) * 14)
            episode = Episode.objects.create(
                podcast=podcast,
                title=ep_title,
                published_at=published,
                duration_seconds=random.randint(20 * 60, 70 * 60),
            )
            # Each episode has a baseline popularity; newer episodes trend higher.
            base = random.randint(80, 400) * (1 + i * 0.15)
            for day_offset in range(days):
                event_date = today - dt.timedelta(days=day_offset)
                if event_date < published:
                    continue
                # Downloads decay as an episode ages past release.
                age = (event_date - published).days
                decay = max(0.2, 1.5 - age * 0.02)
                for platform in platforms:
                    weight = PLATFORM_WEIGHTS.get(platform, 0.5)
                    downloads = max(
                        0, int(base * decay * weight * random.uniform(0.7, 1.3))
                    )
                    listeners = int(downloads * random.uniform(0.55, 0.85))
                    retention = round(random.uniform(38, 78), 1)
                    rows.append(
                        [
                            event_date,
                            podcast.id,
                            episode.id,
                            platform,
                            downloads,
                            listeners,
                            retention,
                        ]
                    )

    client = ensure_schema()
    podcast_ids = list(
        Podcast.objects.filter(owner=user).values_list("id", flat=True)
    )
    if podcast_ids:
        client.command(
            f"ALTER TABLE {EVENTS_TABLE} DELETE WHERE podcast_id IN "
            f"({','.join(str(p) for p in podcast_ids)})"
        )
    client.insert(
        EVENTS_TABLE,
        rows,
        column_names=[
            "event_date",
            "podcast_id",
            "episode_id",
            "platform",
            "downloads",
            "listeners",
            "avg_retention",
        ],
    )
    log(f"Inserted {len(rows):,} analytics rows into ClickHouse.")
    log("Done. Log in with:")
    log(f"  email:    {DEMO_EMAIL}")
    log(f"  password: {DEMO_PASSWORD}")


def _bootstrap_django():
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


if __name__ == "__main__":
    _bootstrap_django()
    seed()
