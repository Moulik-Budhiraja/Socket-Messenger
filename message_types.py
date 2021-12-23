from enum import Enum, auto


class MessageType(Enum):
    MESSAGE = auto()
    DISCONNECT = auto()
    CONNECT = auto()
    REQUEST = auto()
    RESPONSE = auto()
    BLANK = auto()


class RequestType(Enum):
    """
    Enum class for request types.
    """
    FETCH_MESSAGES = auto()
    NEW_GAME = auto()
    GET_POS = auto()
    POST_POS = auto()
    POST_STATE = auto()
    GET_WIN = auto()
