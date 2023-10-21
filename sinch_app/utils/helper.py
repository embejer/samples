from urllib.request import urlopen
from typing import List
from .logger import logger
import uuid
import json

def get_uuid() -> str:
    return str(uuid.uuid4())

def get_current_coordinates() -> List[str]:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    lat, long = str(data['loc']).split(',')
    logger(__name__, level='info', message=f'{get_current_coordinates.__name__}, Current coordinates - ({lat}, {long}).')
    return [lat, long]