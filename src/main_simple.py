from typing import Optional

import fastapi
import uvicorn

api = fastapi.FastAPI()


@api.get('/')
def index():
    body = "<html>" \
           "<body style='padding: 10px;'>" \
           "<h1>Welcome to the API</h1>" \
           "<div>" \
           "Try it: <a href='/api/calculate?x=7&y=11'>/api/calculate?x=7&y=11</a>" \
           "</div>" \
           "</body>" \
           "</html>"

    return fastapi.responses.HTMLResponse(content=body)


@api.get('/api/calculate1')
def calculate1():
    value = 2 + 2
    return {'value': value}


@api.get('/api/calculate2')
def calculate2(x: int, y: int, z: Optional[int] = None):
    if z == 0:
        # return fastapi.Response(content='{"error": "ERROR: z cannot be zero."}',
        #                         media_type="application/json",
        #                         status_code=400)
        return fastapi.responses.JSONResponse(
            content={"error": "ERROR: Z cannot be zero."},
            status_code=400)

    result = x + y
    if z is not None:
        result /= z
    return {
        'x': x,
        'y': y,
        'z': z,
        'value': result
    }

uvicorn.run(api, port=8000, host="127.0.0.1")
