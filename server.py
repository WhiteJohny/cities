import socket
from threading import Thread


class Server(Thread):
    BUFFER_SIZE = 1024

    def __init__(self, address):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('socket created')

        self.sock.bind(address)
        print('socket bound')

        self.sock.listen(2)
        print('socket is listening now')

        self.first_player = None
        self.second_player = None
        self.clients = []

    def __del__(self):
        self.sock.close()

    def run(self):
        while True:
            while len(self.clients) < 2:
                client_sock, client_address = self.sock.accept()
                print(client_sock, client_address)
                self.clients.append(client_sock)

                # if len(self.clients) == 2:
                #     self.first_player = self.clients[0]
                #     self.second_player = self.clients[1]
                #     Thread(target=self.game).start()

            self.first_player = self.clients[0]
            self.second_player = self.clients[1]
            self.game()

    def game(self):
        self.first_player.send("Game is starting!".encode())
        self.first_player.send("Your turn! Enter your city: ".encode())
        self.second_player.send("Game is starting!\nWait for your turn!".encode())

        while True:
            self.circle(self.first_player, self.second_player)
            self.circle(self.second_player, self.first_player)

    @staticmethod
    def circle(player_1, player_2):
        print('receiving')
        city: bytes = player_1.recv(Server.BUFFER_SIZE)
        print('received')
        print(city, player_1)

        print("sending")
        player_2.send(f"Your turn! City:\n{city.decode()}\nEnter your city:  ".encode())
        print("sent")

address = ('localhost', 54678)
server = Server(address)
server.start()
server.join()
