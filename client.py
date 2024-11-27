import socket
from threading import Thread


class Client:
    BUFFER_SIZE = 1024

    def __init__(self, address):
        super().__init__()
        self.last_cities = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Connecting to {}:{}'.format(*address))

        try:
            self.sock.connect(address)
            print('Connected to server')

            data: bytes = self.sock.recv(Client.BUFFER_SIZE)
            print(data.decode('utf-8'))

            Thread(target=self.game).start()
        except Exception:
            print('Server declined connection')

    def game(self):
        while True:
            data: bytes = self.sock.recv(Client.BUFFER_SIZE)
            data: list = data.decode('utf-8').split("\n")
            if len(data) > 2:
                self.last_cities.append(data[1])
            print(*data, sep="\n")

            flag = True
            while flag:
                city = input().upper()
                if not self.last_cities:
                    self.last_cities.append(city)
                    self.sock.send(city.encode())
                    flag = False
                elif city not in self.last_cities and city[0] == self.last_cities[-1][-1]:
                    self.last_cities.append(city)
                    self.sock.send(city.encode())
                    print("City sent!\nWait for your turn!")
                    flag = False
                else:
                    print(f"Enter the correct city!\nLast city: {self.last_cities[-1]}\nAll cities:", end=" ")
                    print(*self.last_cities, sep=" ")


address = ('localhost', 54678)
client = Client(address)
