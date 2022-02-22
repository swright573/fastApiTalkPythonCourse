import asyncio
import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather_api
from models.location import Location
from services import openweather_service, report_service
from views import home


api = fastapi.FastAPI()

def configure():
    configure_routing()
    configure_apikeys()
    configure_fake_data()

def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)

def configure_apikeys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue, please see settings_template.json")
        raise Exception("settings.json file not found, you cannot continue, please see settings_template.json")

    with open('settings.json') as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get('api_key')

def configure_fake_data():
    loc = Location(lat="44", lon="57")
    asyncio.run(report_service.add_report("Windy", loc))
    asyncio.run(report_service.add_report("Wild and wooly", loc))

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
