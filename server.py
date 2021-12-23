import socket
import threading
import pickle
from message import Message
from message_types import RequestType, MessageType


class Data:
    def __init__(self):
        self.data = []
        self.data_user = {}

    def add_data(self, data: Message):
        pass


class Server:
    def __init__(self, ip=socket.gethostbyname(socket.gethostname()), port=5050) -> None:
        self.IP = ip
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def start(self):
        """
            Run when then server starts
            Passes the connection to the handle_client function"""
        print(f"[STARTING] Server is starting on {self.IP}:{self.PORT}")

        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def handle_client(self, conn, addr):
        """
            Handles receiving and sending messages"""
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                msg = Message.decode(msg)
                if msg.type == MessageType.DISCONNECT:
                    connected = False
                    print(f"[DISCONNECT] {msg.author} disconnected.")
                elif msg.type == MessageType.REQUEST:
                    self.handle_request(msg, conn, addr)
                else:
                    print(f"[{msg.author}] {msg.content}")

    def handle_request(self, msg, conn, addr):
        """
            Handles a request from the client"""
        print(f"[{addr}] {msg.content}")
        msg = Message(input(f"[{addr}] "), MessageType.RESPONSE)
        msg.encode()
        conn.send(msg.length)
        conn.send(msg.encoded)


server = Server()
server.start()
