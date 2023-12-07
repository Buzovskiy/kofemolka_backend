from app_settings.poster import Poster
from .models import Location


def import_locations():
    response = Poster().get(url='/api/access.getSpots')

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for obj in response.json()['response']:
        object_defaults = {
            'spot_id': obj['spot_id'],
            'name': '' if obj['name'] is None else obj['name'],
            'spot_name': '' if obj['spot_name'] is None else obj['spot_name'],
            'spot_address': '' if obj['spot_adress'] is None else obj['spot_adress'],
            'region_id': '' if obj['region_id'] is None else obj['region_id'],
            # 'lat': '' if obj['lat'] is None else obj['lat'],
            # 'lng': '' if obj['lng'] is None else obj['lng'],
        }
        obj, created = Location.objects.update_or_create(spot_id=obj['spot_id'], defaults=object_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}
