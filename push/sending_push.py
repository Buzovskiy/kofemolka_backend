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
        if not group:
            return {'error': _('You should specify a group in a message template')}
        clients_stack = [client for client in group.clients.all()]

    responses_200_num = 0
    for client in clients_stack:
        if not client.registration_token:
            continue

        # Сохраняем сообщение в истории сообщений
        message_client = MessageClient.objects.create(
            type=push_template.type,
            client=client,
            title=push_template.title,
            body=push_template.body,
            image=push_template.get_absolute_image_url,
        )

        if push_template.type == 'push_notification_service_quality':
            fcm_message = push_template.build_push_notification_service_quality_message(
                registration_token=client.registration_token,
                order=push_template.order,
                message_client_id=message_client.id
            )
        else:
            fcm_message = push_template.build_push_notification_by_message_template(
                registration_token=client.registration_token
            )

        fcm_response = _send_fcm_message(fcm_message)

        try:
            if fcm_response.ok is True or fcm_response.status_code == 200:
                responses_200_num += 1
                spot_id = None

                if 'spot_id' in fcm_message['message']['data'] and fcm_message['message']['data']['spot_id']:
                    spot_id = fcm_message['message']['data']['spot_id']

                message_client.spot_id = spot_id
                message_client.save()
            else:
                # If the response fails, delete the created MessageClient object
                message_client.delete()

        except AttributeError as e:
            # In case of an unexpected attribute error, also delete the MessageClient object
            message_client.delete()

    total_clients = len(clients_stack)
    return {'total': total_clients, 'success_num': responses_200_num}


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
