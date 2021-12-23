from enum import Enum, auto


class RequestType(Enum):
    """
    Enum class for request types.
    """
    GET_POS = auto()
    POST_POS = auto()
    POST_STATE = auto()
    GET_WIN = auto()
