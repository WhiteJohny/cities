import socket
import threading


class Server:
    ADDRESS = ('localhost', 9000)
    BUFFER_SIZE = 1024
    SEMAPHORE = threading.Semaphore(value=2)

    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket created')

        self.__sock.bind(Server.ADDRESS)
        print('socket bound')

        self.__sock.listen(2)
        print('socket is listening now')

        self.last_cities = []
        self.clients = []
        self.turn = 0
        self.condition = threading.Condition()

    def run(self):
        while True:
            Server.SEMAPHORE.acquire()
            client, address = self.__sock.accept()
            print(f'new connection {address}')
            self.clients.append(client)
            threading.Thread(target=self.check_conn, args=(client, )).start()

    def check_conn(self, conn):
        print("checking connection")
        conn.send('1'.encode())
        print("connection checked")

        print(f"handling {conn}")
        threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def valid_city(self, conn, city):
        if not self.last_cities:
            self.last_cities.append(city)
            return True
        elif city[0] == self.last_cities[-1][-1] and city not in self.last_cities:
            self.last_cities.append(city)
            return True
        else:
            conn.send('This city start with wrong letter or named before'.encode())
            return False
    def game(self, conn, idx):
        while True:
            if self.turn != idx:
                with self.condition:
                    conn.send("Now your opponent turn!".encode())
                    self.condition.wait()

            if len(self.clients) != 2:
                self.handle_client(conn)

            conn.send("Now your turn!".encode())
            timer = threading.Timer(15, self.game_loose, args=(conn, ))
            timer.start()

            flag = True
            stops = False
            while flag:
                try:
                    data: bytes = conn.recv(Server.BUFFER_SIZE)
                except Exception:
                    break

                city: str = data.decode().upper()
                if city == "EXIT":
                    timer.cancel()
                    stops = self.game_stop(conn)
                    break

                if self.valid_city(conn, city):
                    timer.cancel()
                    flag = False

            if not flag:
                data = (f'Your opponent named the city: "{city}"\n'
                                f'You have to name the city starts on letter: "{city[-1]}"').encode()
                self.clients[1 - idx].send(data)
                self.turn = 1 - idx

            with self.condition:
                self.condition.notify()

            if stops:
                break

    def handle_client(self, conn):
        idx = self.clients.index(conn)

        if len(self.clients) == 2:
            conn.send("Game is starting!".encode())
            with self.condition:
                self.condition.notify()
        else:
            conn.send("Waiting for opponent..".encode())
            with self.condition:
                self.condition.wait()
            conn.send("Opponent connected. Game is starting!".encode())

        self.game(conn, idx)

    def game_stop(self, conn):
        self.turn = 0
        self.last_cities = []

        conn.send("You lose!".encode())
        self.clients[1 - self.clients.index(conn)].send("Your opponent left. Yow win!".encode())

        self.clients.remove(conn)
        conn.close()

        Server.SEMAPHORE.release()
        print("game over!|left")

        return True


    def game_loose(self, conn):
        self.turn = self.clients.index(conn)
        self.last_cities = []

        conn.send("You lose!\nNew game is starting!".encode())
        self.clients[1 - self.turn].send("Your opponent did not send the city. Yow win!\nNew game is starting!".encode())

        print("game over!|loose")


server = Server()
server.run()
