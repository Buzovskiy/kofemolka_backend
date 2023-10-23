import requests

SMS_TOKEN = ''
SMS_SIGNATURE = ''


def send_message_ping():
    response = requests.post(
        url=(
                'https://api.turbosms.ua/message/ping?token=%s' %
                SMS_TOKEN
        )
    )
    return response


def send_sms(message, recipients=None, debug=False):
    # if not getattr(settings, 'IS_SMS_ENABLED', False):
    #     if debug:
    #         raise Exception("settings.IS_SMS_ENABLED is not True")
    #     return
    #
    # if not getattr(settings, 'SMS_TOKEN'):
    #     if debug:
    #         raise Exception("settings.SMS_TOKEN is undefined")
    #     return
    #
    # if recipients is None:
    #     recipients = get_default_sms_recipients()
    #
    # if not recipients:
    #     if debug:
    #         raise Exception("no recipients found")
    #     return

    response = requests.post(
        url=(
                'https://api.turbosms.ua/message/send.json?token=%s' %
                SMS_TOKEN
        ),
        json={
            "recipients": recipients,
            "sms": {
                "sender": SMS_SIGNATURE,
                "text": message
            }
        }
    )
    print(1)

    # if response.status_code != 200 and debug:
    #     raise Exception(response.content)
