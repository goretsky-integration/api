from fastapi import FastAPI

import endpoints

__all__ = (
    'app',
)

app = FastAPI()
app.include_router(endpoints.statistics.router, prefix='/v1')
