class UnitIDAPIError(Exception):

    def __init__(self, unit_id: int):
        self.unit_id = unit_id
