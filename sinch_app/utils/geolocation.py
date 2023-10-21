from functools import partial
from geopy.geocoders import Nominatim
from geopy.distance import distance
from typing import List
from .helper import get_uuid, get_current_coordinates
from .logger import logger
import math
import models

def get_details_via_address(location_name: str) -> List[str]:
    try:
        app_name = get_uuid()
        g = Nominatim(user_agent=app_name)
        geocode = partial(g.geocode, language='en')
        location = geocode(location_name)
        logger(__name__, level='info', message=f'{get_details_via_address.__name__}, {location}.')
        return [location.latitude, location.longitude, location.altitude]
    except Exception as error:
        logger(__name__, level='exception', message=f'{get_details_via_address.__name__}, An exception occurred.')

def get_details_via_coordinates(latitude: float, longitude:float) -> str:
    try:
        coordinates = f'{latitude}, {longitude}'
        app_name = get_uuid()
        g = Nominatim(user_agent=app_name)
        reverse = partial(g.reverse, language='en')
        location = reverse(coordinates)
        logger(__name__, level='info', message=f'{get_details_via_coordinates.__name__}, {location}.')
        return location
    except Exception as error:
        logger(__name__, level='exception', message=f'{get_details_via_coordinates.__name__}, An exception occurred.')
        return None

def get_from_current_location(to_location: models.Geolocs) -> int:
    _current_lat, _current_long = get_current_coordinates()
    _current_alt = 0.0
    p1 = (_current_lat, _current_long, _current_alt)
    p2 = (to_location.latitude, to_location.longitude, to_location.altitude)
    return compute_distance(p1, p2)

def get_from_saved_location(from_location: object, to_location: models.Geolocs) -> int:
    p1 = (from_location.latitude, from_location.longitude, from_location.altitude)
    p2 = (to_location.latitude, to_location.longitude, to_location.altitude)
    return compute_distance(p1, p2)


def compute_distance(from_location: tuple, to_location: tuple) -> int:
    flat_distance = distance(from_location[:2], to_location[:2]).km
    euclidian_distance = math.sqrt(flat_distance**2 + (to_location[2] - from_location[2])**2)
    return euclidian_distance