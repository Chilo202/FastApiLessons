
class AppErrors(Exception):
    ''' Базовое исключение '''
    pass


class RoomNotAvailable(AppErrors):
    '''Нету свободных комнат   '''
