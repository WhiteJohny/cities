import threading
import socket


class Client:
    BUFFER_SIZE = 1024
    SERVER_ADDRESS = ('localhost', 9000)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __timeout(self):
        print('Server declined connection')
        self.sock.close()

    def run(self):
        print('Connecting to {}:{}'.format(*Client.SERVER_ADDRESS))
        self.sock.connect(Client.SERVER_ADDRESS)
        timer = threading.Timer(5, self.__timeout)
        timer.start()
        self.__check_conn()
        timer.cancel()
        print('Connected to server')

        th1 = threading.Thread(target=self.receive_messages, args=())
        th1.start()
        th1.join()

    def __check_conn(self):
        self.sock.recv(Client.BUFFER_SIZE)

    def receive_messages(self):
        while True:
            try:
                data: bytes = self.sock.recv(Client.BUFFER_SIZE)
            except ConnectionAbortedError:
                break
            msg: str = data.decode('utf-8')
            print(msg)

            if msg == "Game is starting!":
                th2 = threading.Thread(target=self.send_messages, args=(), daemon=True)
                th2.start()

    def send_messages(self):
        while True:
            msg: str = input()
            data: bytes = msg.encode()
            self.sock.send(data)

            if msg.lower() == "exit":
                print(self.sock.recv(Client.BUFFER_SIZE).decode('utf-8'))
                self.sock.close()


client = Client()

try:
    client.run()
except Exception:
    pass
