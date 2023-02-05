import uvicorn

from core.config import app_settings
from app import get_application

app = get_application()


def main():
    uvicorn.run(
        'main:app',
        port=app_settings.port,
        host=app_settings.host,
        debug=app_settings.is_debug,
        reload=app_settings.is_debug,
    )


if __name__ == '__main__':
    main()
