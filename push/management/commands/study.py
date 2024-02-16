from django.core.management.base import BaseCommand
from django.db import connection
from push.models import MessageClient
from push.serializers import MessageClientSerializer


class Command(BaseCommand):
    help = """Не нужный management command"""

    def handle(self, *args, **options):
        messages = MessageClient.objects.all()
        serializer = MessageClientSerializer(messages, many=True)
        print(serializer.data)
