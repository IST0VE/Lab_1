import socket
import time

# создаем объект сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# определяем хост и порт сервера
host = '127.0.0.1'
port = 12345

# подключаемся к серверу
client_socket.connect((host, port))

# отправляем имя клиента на сервер
client_name = input('Введите ваше имя: ')
client_socket.send(client_name.encode())

while True:
    # отправляем запрос на получение текущего времени
    client_socket.send('time'.encode())

    # получаем ответ от сервера
    response = client_socket.recv(1024).decode()

    # выводим ответ на экран
    print(response)

    # ждем 5 секунд перед отправкой следующего запроса
    time.sleep(5)
