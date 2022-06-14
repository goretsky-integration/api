from pydantic import BaseSettings, Field

__all__ = (
    'app_settings',
)


class AppSettings(BaseSettings):
    port: int = Field(..., env='APP_PORT')
    host: str = Field(..., env='APP_HOST')


app_settings = AppSettings()
