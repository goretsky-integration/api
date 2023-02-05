from fastapi import Depends

from api import common_schemas
from core import config
from services.http_client_factories import closing_dodo_is_api_client_factory
from api.v2.bearer import AccessTokenBearer


def get_closing_dodo_is_api_client(
        *,
        country_code: common_schemas.CountryCode,
        token: str = Depends(AccessTokenBearer()),
):
    return closing_dodo_is_api_client_factory(
        country_code=country_code.value,
        token=token,
        app_user_agent=config.APP_USER_AGENT,
    )
