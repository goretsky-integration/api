from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

__all__ = ('include_exception_handlers',)


async def unauthorized_error_handler(request: Request, exc):
    return JSONResponse(
        content={'detail': 'Unauthorized'},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def include_exception_handlers(app: FastAPI) -> None:
    pass
