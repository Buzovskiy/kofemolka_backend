import requests


class Turbosms:
    sms_token = ''
    sms_signature = ''

    def __init__(self, sms_token, sms_signature):
        self.sms_token = sms_token
        self.sms_signature = sms_signature

    def send_message_ping(self):
        response = requests.post(url=('https://api.turbosms.ua/message/ping?token=%s' % self.sms_token))
        return response

    def send_sms(self, message, recipients) -> dict:
        """
        Method that sends SMS message to the list of recipients
        :param string message:
        :param list recipients:
        :return: dict
        """

        response = requests.post(
            url=('https://api.turbosms.ua/message/send.json?token=%s' % self.sms_token),
            json={
                "recipients": recipients,
                "sms": {
                    "sender": self.sms_signature,
                    "text": message
                }
            }
        )
        return response
