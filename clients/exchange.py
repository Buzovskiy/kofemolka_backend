from app_settings.poster import Poster
from .models import Clients


def import_clients():
    response = Poster().get(url='/api/clients.getClients')

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for client in response.json()['response']:
        client_defaults = prepare_client_data(client)
        obj, created = Clients.objects.update_or_create(
            client_id=client['client_id'], defaults=client_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}


def prepare_client_data(client_data):
    """
    :param client_data: dictionary with key values corresponding to client data
    :return: dictionary with client data which are to add to the database
    """
    data = {
        'client_id': client_data['client_id'],
        'firstname': client_data['firstname'],
        'lastname': client_data['lastname'],
    }
    return data
