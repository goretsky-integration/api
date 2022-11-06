from fastapi import HTTPException, status

__all__ = (
    'BadRequest',
    'Unauthorized',
)


class BadRequest(HTTPException):

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class Unauthorized(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
        )
