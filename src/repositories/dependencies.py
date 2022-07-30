from repositories.office_manager import OfficeManagerRepository

__all__ = (
    'get_office_manager_repository',
)


def get_office_manager_repository() -> OfficeManagerRepository:
    return OfficeManagerRepository('https://officemanager.dodopizza.ru/')
