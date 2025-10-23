class AppErrors(Exception):

    detail = "Unexpected Error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppErrors):
    detail = "Object not found"


class AllRoomsAreBookedException(AppErrors):
    detail = "No available room for booking"


class DuplicateEntryError(AppErrors):
    detail = "Record with this unique value already exists."