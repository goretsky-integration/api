from fastapi import FastAPI
from fastapi.responses import JSONResponse

import endpoints
from utils import exceptions

__all__ = (
    'app',
)

app = FastAPI()
app.include_router(endpoints.v2.statistics.router)
app.include_router(endpoints.v1.statistics.router)
app.include_router(endpoints.v2.stop_sales.router)
app.include_router(endpoints.ping.router)


@app.exception_handler(exceptions.PrivateDodoAPIError)
async def on_private_dodo_api_error(request, exc: exceptions.PrivateDodoAPIError):
    return JSONResponse({'error': 'error'}, status_code=exc.status_code)
