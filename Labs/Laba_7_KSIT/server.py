import socketserver
import datetime

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # При подключении клиента, сервер ждет его сообщения с именем
        name = self.request.recv(1024).strip().decode('utf-8')
        print(f"{name} подключился")
        while True:
            # Получаем текущее время
            now = datetime.datetime.now().strftime("%H:%M:%S")
            # Отправляем сообщение с именем и временем клиенту
            self.request.sendall(f"{name} сейчас {now}".encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Ожидание подключения...")
        server.serve_forever()
