import socket
from message import Message
from message_types import RequestType, MessageType


class Client:
    def __init__(self, server_ip: str, server_port=5050) -> None:
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

    def connect(self) -> None:
        """
            Establishes a connection to the server"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def disconnect(self, author) -> None:
        """
            Sends a message to the server to disconnect"""
        self.send(author, type=MessageType.DISCONNECT)

    def send(self, author, msg: str = '', type=MessageType.MESSAGE) -> None:
        """
            Sends a message to the server"""
        msg = Message(author, msg, type)
        msg.encode()
        self.client.send(msg.length)
        self.client.send(msg.encoded)

    def request(self, msg: str, msg_type: RequestType) -> Message:
        """
            Sends a request to the server and returns the response"""
        self.send(msg, MessageType.REQUEST)
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            msg = Message.decode(msg)
            return msg
        else:
            return Message(type=MessageType.BLANK)


if __name__ == '__main__':
    client = Client(socket.gethostbyname(socket.gethostname()))
    client.connect()
    client.send(input("Enter a message: "))
    client.disconnect()
