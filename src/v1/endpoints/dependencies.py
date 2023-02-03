from fastapi import Request

from core import config
from services.http_client_factories import closing_public_api_client_factory, closing_office_manager_api_client_factory, \
    HTTPClient, closing_shift_manager_api_client_factory

__all__ = (
    'get_closing_public_api_client',
    'get_closing_office_manager_api_client',
    'get_closing_shift_manager_api_client',
)


def get_closing_public_api_client(*, country_code: str) -> HTTPClient:
    return closing_public_api_client_factory(country_code=country_code, app_user_agent=config.APP_USER_AGENT)


def get_closing_office_manager_api_client(*, request: Request, country_code: str) -> HTTPClient:
    return closing_office_manager_api_client_factory(
        cookies=request.cookies,
        country_code=country_code,
        app_user_agent=config.APP_USER_AGENT,
    )


def get_closing_shift_manager_api_client(*, request: Request, country_code: str) -> HTTPClient:
    return closing_shift_manager_api_client_factory(
        cookies=request.cookies,
        country_code=country_code,
        app_user_agent=config.APP_USER_AGENT,
    )
