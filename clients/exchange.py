from app_settings.poster import Poster
from .models import Clients


def import_clients():
    response = Poster().get(url='/api/clients.getClients')

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for client in response.json()['response']:
        client_defaults = {
            'client_id': client['client_id'],
            'firstname': client['firstname'],
            'lastname': client['lastname'],
        }
        obj, created = Clients.objects.update_or_create(
            client_id=client['client_id'], defaults=client_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}
