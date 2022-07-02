from fastapi import FastAPI
from fastapi.responses import JSONResponse

import endpoints
from utils import exceptions

__all__ = (
    'app',
)

app = FastAPI()
app.include_router(endpoints.statistics.router, prefix='/v1')
app.include_router(endpoints.stop_sales.router, prefix='/v1')


@app.exception_handler(exceptions.PrivateDodoAPIError)
async def on_private_dodo_api_error(request, exc: exceptions.PrivateDodoAPIError):
    return JSONResponse({'error': 'error'}, status_code=exc.status_code)
