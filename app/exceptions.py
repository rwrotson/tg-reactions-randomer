from app.modes import ChatOrChannelMode as Mode


class NotAllParamsException(Exception):
    """Raised when script doesn't get all needed params from args or envs"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CustomValueException(Exception):
    """Raised when provided params do not make sense"""

    def __init__(self, message: str):
        super().__init__(message)


class EntityNotFoundException(Exception):
    """Raised when chat or channel is not found"""

    def __init__(self, entity_id: int, mode: Mode):
        message = f'{mode.upper()} {entity_id} WAS NOT FOUND'
        super().__init__(message)
