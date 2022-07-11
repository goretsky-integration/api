class PublicDodoAPIError(Exception):
    pass


class DodoISAPIError(Exception):
    pass


class PrivateDodoAPIError(Exception):

    def __init__(self, *args, status_code: int, **kwargs):
        self.status_code = status_code


class PartialStatisticsAPIError(DodoISAPIError):

    def __init__(self, *args, unit_id: int | str, **kwargs):
        self.unit_id = unit_id
        super(*args, **kwargs)


class OperationalStatisticsAPIError(PublicDodoAPIError):

    def __init__(self, *args, unit_id: int | str, **kwargs):
        self.unit_id = unit_id
        super(*args, **kwargs)


class DoesNotExistInCache(Exception):

    def __init__(self, *args, key: str, **kwargs):
        self.key = key
        super(*args, **kwargs)

    def __str__(self):
        return f'Object with {self.key=} has not been found'
