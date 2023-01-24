import contextlib
from typing import TypeAlias

import httpx

__all__ = (
    'closing_dodo_is_api_client_factory',
    'closing_office_manager_api_client_factory',
    'closing_public_api_client_factory',
    'HTTPClient',
)

HTTPClient: TypeAlias = httpx.AsyncClient


@contextlib.asynccontextmanager
async def closing_dodo_is_api_client_factory(*, token: str, country_code: str, app_user_agent: str) -> HTTPClient:
    base_url = f'https://api.dodois.io/dodopizza/{country_code}/'
    headers = {'User-Agent': app_user_agent, 'Authorization': f'Bearer {token}'}
    async with httpx.AsyncClient(headers=headers, base_url=base_url, timeout=120) as client:
        yield client


@contextlib.asynccontextmanager
async def closing_public_api_client_factory(*, country_code: str, app_user_agent: str) -> HTTPClient:
    base_url = f'https://publicapi.dodois.io/{country_code}/api/v1/'
    headers = {'User-Agent': app_user_agent}
    async with httpx.AsyncClient(headers=headers, base_url=base_url, timeout=120) as client:
        yield client


@contextlib.asynccontextmanager
async def closing_office_manager_api_client_factory(*, country_code: str, app_user_agent: str) -> HTTPClient:
    base_url = f'https://officemanager.dodopizza.{country_code}/'
    headers = {'User-Agent': app_user_agent}
    async with httpx.AsyncClient(headers=headers, base_url=base_url, timeout=120) as client:
        yield client
