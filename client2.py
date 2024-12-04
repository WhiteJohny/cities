import threading
import socket


class Client:
    BUFFER_SIZE = 1024
    SERVER_ADDRESS = ('localhost', 9000)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    def run(self):
        print('Connecting to {}:{}'.format(*Client.SERVER_ADDRESS))
        self.sock.connect(Client.SERVER_ADDRESS)
        timer = threading.Timer(15, self.timeout)
        timer.start()
        self.check_conn()
        timer.cancel()
        print('Connected to server')

        th1 = threading.Thread(target=self.receive_messages, args=())
        th2 = threading.Thread(target=self.send_messages, args=())

        th2.start()
        th1.start()

        th1.join()

    def timeout(self):
        print('Server declined connection')
        self.sock.close()

    def check_conn(self):
        self.sock.recv(Client.BUFFER_SIZE)

    def receive_messages(self):
        while True:
            try:
                data: bytes = self.sock.recv(Client.BUFFER_SIZE)
            except Exception:
                self.sock.close()
                break
            msg: str = data.decode('utf-8')
            print(msg)

    def send_messages(self):
        while True:
            msg: str = input()
            data: bytes = msg.encode()
            self.sock.send(data)
            print("Sent")

            if msg.lower() == "exit":
                print(self.sock.recv(Client.BUFFER_SIZE).decode('utf-8'))
                self.sock.close()
                break


client = Client()

try:
    client.run()
except Exception:
    pass
