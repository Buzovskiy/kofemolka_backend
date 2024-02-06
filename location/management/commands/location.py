from django.core.management.base import BaseCommand, CommandError
from location.utils import get_location_or_create


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        location = get_location_or_create(spot_id=1)
        print(location)
