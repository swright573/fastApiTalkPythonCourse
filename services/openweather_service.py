from typing import Optional
import httpx
from httpx import Response

from infrastructure import weather_cache
from models.validation_error import ValidationError

api_key: Optional[str] = None

async def get_report_async(lat: str, lon: str, units: str) -> dict:
    lat, lon, units = validate_units(lat, lon, units)

    if forecast := weather_cache.get_weather(lat, lon, units):
        return forecast

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    forecast = data['main']
    weather_cache.set_weather(lat, lon, units, forecast)

    return forecast

def validate_units(lat, lon, units):   # validate lat, long, and units are valid ... raise ValidationError if not
    # do validation
    return lat, lon, units

'''
api.openweathermap.org / data / 2.5 / weather?lat = {lat} & lon = {lon} & appid = {API key}

Parameters
lat, lon 	required 	Geographical coordinates (latitude, longitude).
If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around,
    please use our Geocoding API.

Pickering/Coordinates
43.8384° N, 79.0868° W
43 -79

appid 	required 	Your unique API key (you can always find it on your account page under the "API key" tab)
mode 	optional 	Response format. Possible values are xml and html. If you don't use the mode parameter format is 
                    JSON by default. Learn more
units 	optional 	Units of measurement. standard, metric and imperial units are available. If you do not use the 
                   units parameter, standard units will be applied by default.
lang 	optional 	You can use this parameter to get the output in your language. Learn more
'''