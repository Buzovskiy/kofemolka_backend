from .models import Clients
from app_settings.poster import Poster
from clients.exchange import prepare_client_data


def get_client_or_create(client_id):
    """
    Returns a client
    :param client_id: ID in Poster
    :return: client object or None
    """
    try:
        client = Clients.objects.get(client_id=client_id)
    except Clients.DoesNotExist:
        # If client does not exist request client in Poster and save it
        response = Poster().get(url='/api/clients.getClient', params={'client_id': client_id})
        if 'error' in response:
            return None

        if 'response' in response.json() and len(response.json()['response']):
            client_remote = response.json()['response'][0]
            client_data = prepare_client_data(client_remote)
            client = Clients.objects.create(**client_data)
        else:
            return None

    return client
