from typing import Optional, Tuple

from fastapi import HTTPException
import httpx
from httpx import Response
import json

from infrastructure import weather_cache
from models.validation_error import ValidationError

api_key: Optional[str] = None

async def get_weather_async(city: str, state: Optional[str], country: str, units: str) -> dict:
    city, state, country, units = validate(city, state, country, units)

    if forecast := weather_cache.get_weather(city, state, country, units):
        return forecast

    geostate = 'xx' if not state else state   # geo lookup seems to require state be something, even if only xx
    url = f'https://api.openweathermap.org/geo/1.0/direct?q={city},{geostate},{country}&limit=1&appid={api_key}'

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = json.loads(resp.content.decode('utf-8')[1:-1])
    lat = data['lat']
    lon = data['lon']

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    forecast = data['main']

    weather_cache.set_weather(city, state, units, country, forecast)

    return forecast

def validate(city: str, state: Optional[str], country: Optional[str], units: str) -> Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()

    country = "CA" if not country else country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as CA or US."
        raise ValidationError(status_code=400, error_msg=error)

    if state:   # actually province :-)
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid 'state': {state}. It must be a two letter abbreviation such as ON or BC."
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units

'''
api.openweathermap.org / data / 2.5 / weather?lat = {lat} & lon = {lon} & appid = {API key}

Parameters
lat, lon 	required 	Geographical coordinates (latitude, longitude).
If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around,
    please use our Geocoding API.

Pickering/Coordinates
43.8384° N, 79.0868° W
43.8384 -79.0868

appid 	required 	Your unique API key (you can always find it on your account page under the "API key" tab)
mode 	optional 	Response format. Possible values are xml and html. If you don't use the mode parameter format is 
                        JSON by default.
units 	optional 	Units of measurement. standard, metric and imperial units are available. If you do not use the 
                        units parameter, standard units will be applied by default.
lang 	optional 	You can use this parameter to get the output in your language.
'''