from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from push.models import Message, MessageClient
from order.models import Transaction
from push.messaging import _send_fcm_message

from app_settings.models import AppSettings
from push.sending_push import send_push_by_message_template


class Command(BaseCommand):
    help = """
    Send push on message template.
    Reciever can be client or group.
    example: python manage.py send_push_message_template --message_id 2 --receiver client
    """

    def add_arguments(self, parser):
        parser.add_argument("--message_id", required=True)
        parser.add_argument("--receiver", required=True)

    def handle(self, *args, **options):
        message_id = options["message_id"]
        receiver = options["receiver"]
        result = send_push_by_message_template(message_id, receiver)
        print(result)

