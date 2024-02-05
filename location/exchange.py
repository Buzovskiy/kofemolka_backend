from app_settings.poster import Poster
from .models import Location


def import_locations():
    response = Poster().get(url='/api/access.getSpots')

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for obj in response.json()['response']:
        object_defaults = prepare_location_data(obj)
        obj, created = Location.objects.update_or_create(spot_id=obj['spot_id'], defaults=object_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}


def prepare_location_data(location_data):
    """
    :param location_data: dictionary with key values corresponding to location data
    :return: dictionary with location data which are to add to the database
    """
    data = {
        'spot_id': location_data['spot_id'],
        'name': '' if location_data['name'] is None else location_data['name'],
        'spot_name': '' if location_data['spot_name'] is None else location_data['spot_name'],
        'spot_address': '' if location_data['spot_adress'] is None else location_data['spot_adress'],
        'region_id': '' if location_data['region_id'] is None else location_data['region_id'],
    }
    return data
