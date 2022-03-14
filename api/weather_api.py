from typing import Optional, List

import fastapi
import asyncio
from fastapi import Depends
from fastapi.responses import PlainTextResponse

import logging

from starlette.requests import Request

from models.location import Location
from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from services import openweather_service, report_service

router = fastapi.APIRouter()

@router.get('/api/weather/{city}')
async def weather(loc: Location = Depends(), units: Optional[str] = 'metric'):
    # if you say loc: Location, it only pulls data from http post of bodies
    # if you want it to look in the querystring (and maybe elsewhere) you should say loc: Location = Depends()
    #   Depends() is a shortform for Depends(Location) in this case to avoid repeating Location
    try:
        return await openweather_service.get_weather_async(loc.city, loc.state, loc.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)

    except Exception as x:
        print(f'Server crashed while processing request: {x}')
        return fastapi.Response(content="Error processing your request", status_code=500)

@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    return await report_service.get_reports()

@router.post('/api/reports', name='add_report', status_code=201, response_model=Report)
async def reports_post(report_submittal: Report) -> Report:
    d = report_submittal.description
    loc = report_submittal.location
    return await report_service.add_report(d, loc)

# added to test async concurrency
@router.get('/api/testasync', name='test_async', response_class=PlainTextResponse)
async def test_async(request: Request):
    logging.basicConfig(level=logging.DEBUG)
    client_host = request.client.host
    await run_functions(client_host)
    return PlainTextResponse(content='Susan Wright', status_code=200)

async def function1(host):
    logging.info(f'Client is {host}. Started function1().')
    await asyncio.sleep(3)
    logging.info(f'Client is {host}. Finished function1().')
    return

async def function2(host):
    logging.info(f'Client is {host}. Started function2().')
    await asyncio.sleep(1)
    logging.info(f'Client is {host}. Finished function2().')
    return

async def function3(host):
    logging.info(f'Client is {host}. Started function3().')
    await asyncio.sleep(5)
    logging.info(f'Client is {host}. Finished function3().')
    return

async def run_functions(host):
    await function1(host)
    await function2(host)
    await function3(host)
