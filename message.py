import pickle
from message_types import MessageType


class Message:
    def __init__(self, author, content='', type=MessageType.MESSAGE, header_length=64, header_format='utf-8') -> None:
        self.author = author
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
