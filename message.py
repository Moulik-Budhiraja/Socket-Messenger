import pickle
from enum import Enum, auto


class MessageType(Enum):
    MESSAGE = auto()
    DISCONNECT = auto()
    CONNECT = auto()
    REQUEST = auto()
    RESPONSE = auto()


class Message:
    def __init__(self, content='', type=MessageType.MESSAGE, header_length=64, header_format='utf-8') -> None:
        self.content = content
        self.type = type
        self.HEADER_LENGTH = header_length
        self.HEADER_FORMAT = header_format

    def encode(self) -> bytes:
        message = pickle.dumps(self)
        self.length = len(message)
        self.length = str(self.length).encode(self.HEADER_FORMAT)
        self.length += b' ' * (self.HEADER_LENGTH - len(self.length))

        self.encoded = message
        return message

    @staticmethod
    def decode(encoded_msg: bytes) -> "Message":
        return pickle.loads(encoded_msg)
