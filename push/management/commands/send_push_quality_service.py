from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from push.models import Message, MessageClient
from order.models import Transaction
from push.messaging import _send_fcm_message

from app_settings.models import AppSettings


class Command(BaseCommand):
    # help = "Closes the specified poll for voting"
    #
    def add_arguments(self, parser):
        parser.add_argument("--mode", required=False)

    def handle(self, *args, **options):
        mode = options["mode"]
        push_template = Message.objects.filter(type__exact='push_notification_service_quality').first()
        if push_template is None:
            return False
        try:
            t1 = AppSettings.objects.get(key='t1_service_quality_polling_push').value
            t2 = AppSettings.objects.get(key='t2_service_quality_polling_push').value
            if not t1 or not t2:
                return False
            t1 = int(t1)
            t2 = int(t2)
        except (AppSettings.DoesNotExist, ValueError):
            return False

        order_queryset = Transaction.objects.filter(push_is_sent=False)
        order_queryset = order_queryset.filter(created_at__lt=(timezone.now() - timedelta(seconds=t1)))
        order_queryset = order_queryset.exclude(client__registration_token__exact='')
        order_queryset = order_queryset.exclude(client__registration_token__isnull=True)
        for order in order_queryset.all():
            message_history_qs = MessageClient.objects.filter(client=order.client)
            message_history_qs = message_history_qs.filter(message__type__exact='push_notification_service_quality')
            message_history_qs = message_history_qs.filter(created_at__gt=(timezone.now() - timedelta(seconds=t2)))
            if message_history_qs.count():
                """
                Если есть хотя бы одно сообщение в истории сообщений типа push_notification_service_quality, которое
                было отправлено позже нынешнего времени минус t2, то считаем, что еще не пришло время отправлять
                клиенту новый push типа push_notification_service_quality.
                """
                continue
            fcm_message = push_template.build_push_notification_service_quality_message(
                registration_token=order.client.registration_token
            )
            fcm_response = _send_fcm_message(fcm_message)
            try:
                if fcm_response.ok is True or fcm_response.status_code == 200:
                    # Для транзакции (заказа в заведении) отмечаем, что сообщение доставлено
                    order.push_is_sent = True
                    order.save()
                    # Сохраняем сообщение в истории сообщений
                    MessageClient.objects.create(
                        message=push_template,
                        client=order.client
                    )
            except AttributeError:
                pass