import datetime

from fastapi import Depends, Query

from core import config
from v2.endpoints.bearer import AccessTokenBearer
from v2.periods import Period
from services.http_client_factories import closing_dodo_is_api_client_factory


def get_closing_dodo_is_api_client(
        *,
        country_code: str,
        token: str = Depends(AccessTokenBearer()),
):
    return closing_dodo_is_api_client_factory(
        country_code=country_code,
        token=token,
        app_user_agent=config.APP_USER_AGENT,
    )


def get_period(
        *,
        start: datetime.datetime = Query(),
        end: datetime.datetime = Query(),
) -> Period:
    return Period(start=start, end=end)
