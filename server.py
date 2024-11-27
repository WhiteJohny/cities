import socket
from threading import Thread


# AF address family: ipv4, ipv6, unix bluetooth,
# 32 bit
# 255.255.255.255
# 8 8 8 8
# 256 [0, 255]


class Server(Thread):
	EOF = b'///'
	BUFFER_SIZE = 10

	def __init__(self, address):
		super().__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # STREAM TCP/ DGRAM UDP
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print('Socket created')
		self.sock.bind(address)
		print('Socket binded')
		self.sock.listen(1)
		print('Socket now listening')
		self.clients = set()

		# queue

	def __del__(self):
		self.sock.close()
	
	# worker queue
	# while True
	# queue get
	# data -> to all

	def run(self):
		while True:
			client_sock, client_address = self.sock.accept()
			print(client_sock, client_address)
			self.clients.add(client_sock)
			Thread(target=self.chatting, args=(client_sock,), daemon=True).start()

	def chatting(self, conn):
		while True:
			# get
			print('receiving')
			data: bytes = self.recv(conn)
			# queue put data
			print('received')
			# processing
			print('processing')
			text: str = data.decode('utf-8').upper()
			if text == 'EXIT':
				print('exit...')
				break
			print(text)
			data: bytes = text.encode('utf-8')
			print('sending')
			# send
			self.send(conn, data)
			print('sent')

	@staticmethod
	def send(conn: socket.socket, data: bytes):
		conn.send(data)
		conn.send(Server.EOF)

	@staticmethod
	def recv(conn: socket.socket) -> bytearray:
		result = bytearray()
		while True:
			data: bytes = conn.recv(Server.BUFFER_SIZE)
			result.extend(data)
			if not data:
				break
			if result[-3:] == Server.EOF:
				break
		return result[:-3]


# with open('filedfgd', 'wb') as file:
# 	file.write(result)

address = ('localhost', 9000)
server = Server(address)
server.start()
server.join()
