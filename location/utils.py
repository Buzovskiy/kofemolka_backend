from app_settings.poster import Poster
from .models import Location
from location.exchange import prepare_location_data


def get_location_or_create(spot_id):
    """
    Returns a location
    :param spot_id: ID in Poster
    :return: location object or None
    """
    try:
        location = Location.objects.get(spot_id=spot_id)
    except Location.DoesNotExist:
        # If location does not exist request location in Poster and save it
        response = Poster().get(url='/api/spots.getSpot', params={'spot_id': spot_id})
        if 'error' in response:
            return None

        if 'response' in response.json() and len(response.json()['response']):
            object_remote = response.json()['response']
            object_data = prepare_location_data(object_remote)
            location = Location.objects.create(**object_data)
        else:
            return None

    return location


