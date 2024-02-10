from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    # help = "Closes the specified poll for voting"
    #
    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        f = open(settings.BASE_DIR / "demofile3.txt", "a")
        time = timezone.now().strftime('%X')
        f.write(time + '\n')
        f.close()
        self.stdout.write(
            self.style.SUCCESS('Successfully closed poll')
        )
