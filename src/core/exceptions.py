from fastapi import HTTPException, status

__all__ = (
    'BadRequest',
    'Unauthorized',
    'UnitIDAPIError',
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


class UnitIDAPIError(Exception):

    def __init__(self, unit_id: int):
        self.unit_id = unit_id
