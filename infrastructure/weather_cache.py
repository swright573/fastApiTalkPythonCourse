import datetime
from typing import Optional, Tuple

__cache = {}  # could use redis or another tool, using memory as a simple solution here
lifetime_in_hours = 1.0


def get_weather(lat: str, lon: str, units: str) -> Optional[dict]:
    key = __create_key(lat, lon, units)
    data: dict = __cache.get(key)
    if not data:
        return None

    data: dict = __cache.get(key)
    if not data:
        return None

    last = data['time']
    dt = datetime.datetime.now() - last
    if dt / datetime.timedelta(minutes=60) < lifetime_in_hours:
        return data['value']

    del __cache[key]
    return None


def set_weather(lat: str, lon: str, units: str, value: dict):
    key = __create_key(lat, lon, units)
    data = {
        'time': datetime.datetime.now(),
        'value': value
    }
    __cache[key] = data
    __clean_out_of_date()


def __create_key(lat: str, lon: str, units: str) -> Tuple[str, str, str]:
    if not lat or not lon or not units:
        raise Exception("Latitude, longitude, and units are required")

    return lat.strip().lower(), lon.strip().lower(), units.strip().lower()


def __clean_out_of_date():
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get('time')
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
