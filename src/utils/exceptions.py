class PublicDodoAPIError(Exception):
    pass


class OperationalStatisticsAPIError(PublicDodoAPIError):

    def __init__(self, *args, unit_id: int | str, **kwargs):
        self.unit_id = unit_id
        super(*args, **kwargs)
