import httpx

__all__ = (
    'APIClientRepository',
)


class APIClientRepository:

    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=60)

    async def close(self):
        if not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
