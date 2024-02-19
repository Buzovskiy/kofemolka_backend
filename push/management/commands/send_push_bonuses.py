from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from push.models import Message, MessageClient
from order.models import Transaction
from push.messaging import _send_fcm_message

from app_settings.models import AppSettings
from push.sending_push import send_push_on_bonuses_for_transaction


class Command(BaseCommand):
    help = """
    Send push on bonuses for transaction
    example: python manage.py send_push_bonuses --client_id 22 --bonuses_amount 10.2
    """

    def add_arguments(self, parser):
        parser.add_argument("--client_id", required=True)
        parser.add_argument("--bonuses_amount", required=True)

    def handle(self, *args, **options):
        client_id = options["client_id"]
        bonuses_amount = options["bonuses_amount"]
        result = send_push_on_bonuses_for_transaction(client_id, bonuses_amount)
        print(result)

