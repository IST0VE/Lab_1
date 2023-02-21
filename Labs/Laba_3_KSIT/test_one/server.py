import socket
import datetime

# Настройки сервера
IP = "127.0.0.1"
PORT = 20001

# Создаем сокет
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # Привязываем сокет к IP и PORT
    server_socket.bind((IP, PORT))
    print("[INFO] Server is ready and waiting for clients...")

    # Бесконечный цикл, чтобы прослушивать клиентов
    while True:
        # Принимаем данные от клиента
        data, address = server_socket.recvfrom(1024)
        data = data.decode("utf-8")
        
        # Проверяем, является ли запрос о времени
        if data == "Show time":
            # Отправляем текущее время клиенту
            time = str(datetime.datetime.now().time())
            server_socket.sendto(time.encode("utf-8"), address)
        else:
            # Если запрос не является запросом о времени, то завершаем работу сервера
            print("[INFO] Closing server...")
            break
