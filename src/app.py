from fastapi import FastAPI, status, Response

import v1.endpoints
import v2.endpoints

__all__ = (
    'app',
)

app = FastAPI()
app.include_router(v1.endpoints.reports.router)
app.include_router(v2.endpoints.reports.router)
app.include_router(v1.endpoints.stop_sales.router)
app.include_router(v2.endpoints.stop_sales.router)
app.include_router(v1.endpoints.stocks.router)
app.include_router(v1.endpoints.orders.router)


@app.get('/ping')
async def ping():
    return Response(status_code=status.HTTP_200_OK)
