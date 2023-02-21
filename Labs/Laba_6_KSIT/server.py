import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        name = data.decode().strip()
        if not hasattr(self, 'clients'):
            self.clients = []
        self.clients.append((name, socket[0], socket[1]))
        if len(self.clients) == 1:
            message = f"{name}, your IP: {socket[0]}, port: {socket[1]}"
        else:
            message = f"The length of your name, {name}, is {len(name)}"
        socket.sendto(message.encode(), socket)

if __name__ == "__main__":
    with socketserver.UDPServer(('localhost', 20001), MyUDPHandler) as server:
        print('Server started, waiting for clients')
        server.serve_forever()
