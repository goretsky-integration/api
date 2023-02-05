from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

__all__ = (
    'AccessTokenBearer',
)


class AccessTokenBearer(HTTPBearer):

    def __init__(self):
        super().__init__(scheme_name='Token', description='Access Token к Dodo API')

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        return credentials.credentials
