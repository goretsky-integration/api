import uvicorn

from core.config import app_settings
from app import app


def main():
    uvicorn.run(
        'app:app',
        port=app_settings.port,
        host=app_settings.host,
    )


if __name__ == '__main__':
    main()
