from django.core.management.base import BaseCommand

from pipeline.seed import seed


class Command(BaseCommand):
    help = "Seed demo podcasts and episodes (Postgres) and analytics (ClickHouse)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Number of days of analytics history to generate.",
        )

    def handle(self, *args, **options):
        seed(days=options["days"], log=self.stdout.write)
