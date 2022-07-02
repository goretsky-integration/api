class PublicDodoAPIError(Exception):
    pass


class DodoISAPIError(Exception):
    pass


class PrivateDodoAPIError(Exception):

    def __init__(self, *args, status_code: int, **kwargs):
        self.status_code = status_code


class KitchenStatisticsError(DodoISAPIError):

    def __init__(self, *args, unit_id: int | str, **kwargs):
        self.unit_id = unit_id
        super(*args, **kwargs)


class OperationalStatisticsAPIError(PublicDodoAPIError):

    def __init__(self, *args, unit_id: int | str, **kwargs):
        self.unit_id = unit_id
        super(*args, **kwargs)
