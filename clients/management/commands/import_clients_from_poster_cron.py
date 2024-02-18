from django.core.management.base import BaseCommand
from clients.exchange import import_clients


class Command(BaseCommand):
    help = """
    python manage.py import_clients_from_poster_cron: 
    Run this script as a cron job for clients import from poster database
    """

    def handle(self, *args, **options):
        import_clients()
