from datetime import timedelta, datetime
from django.db import connection
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from push.models import Message, MessageClient
from push.messaging import _send_fcm_message
from clients.models import Clients


def send_push_by_message_template(message_id, receiver):
    try:
        push_template = Message.objects.get(pk=message_id)
    except ObjectDoesNotExist as e:
        print(e)
        return {'error': e}

    clients_stack = []
    if receiver == 'client':
        client = push_template.client
        if not client:
            return {'error': _('You should specify a client')}
        clients_stack.append(client)
    elif receiver == 'group':
        group = push_template.push_group
        clients_stack = [client for client in group.clients.all()]

    responses_200_num = 0
    for client in clients_stack:
        if not client.registration_token:
            continue
        fcm_message = push_template.build_push_notification_by_message_template(
            registration_token=client.registration_token
        )

        fcm_response = _send_fcm_message(fcm_message)

        try:
            if fcm_response.ok is True or fcm_response.status_code == 200:
                responses_200_num += 1
                # Сохраняем сообщение в истории сообщений
                MessageClient.objects.create(
                    type=push_template.type,
                    client=client,
                    title=fcm_message['message']['data']['title'],
                    body=fcm_message['message']['data']['body'],
                    image=fcm_message['message']['data']['image']
                )
            # print(fcm_response.json())
        except AttributeError as e:
            continue



def send_push_on_bonuses_for_transaction(client_id, bonuses_amount):
    try:
        client = Clients.objects.get(client_id=client_id)
        push_template = Message.objects.get(type__exact='push_notification_bonus')
    except ObjectDoesNotExist as e:
        return {'error': e}

    if client.do_not_send_push_bonus:
        return {'error': 'Send push bonus to client is disabled'}

    try:
        bonuses_amount = float(bonuses_amount)
    except ValueError as e:
        return {'error': e}

    if not client.registration_token:
        return {'error': f'Client with client_id {client_id} does not has registration token'}

    fcm_message = push_template.build_push_notification_bonus_for_transaction(
        registration_token=client.registration_token,
        bonuses_amount=bonuses_amount
    )

    fcm_response = _send_fcm_message(fcm_message)
    try:
        if fcm_response.ok is True or fcm_response.status_code == 200:
            # Сохраняем сообщение в истории сообщений
            MessageClient.objects.create(
                type=push_template.type,
                client=client,
                title=fcm_message['message']['data']['title'],
                body=fcm_message['message']['data']['body'],
                image=fcm_message['message']['data']['image']
            )
            return {'success': 'The push notification is sent successfully'}
        else:
            print(fcm_response.json())
            return {'error': 'The push notification is not sent'}
    except AttributeError as e:
        return {'error': e}
