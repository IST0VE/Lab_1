import socket

# создаем объект сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# определяем хост и порт сервера
host = '127.0.0.1'
port = 12345

# соединяемся с сервером
client_socket.connect((host, port))

# получаем сообщение от пользователя
message = input('Введите сообщение: ')

# отправляем сообщение серверу
client_socket.send(message.encode())

# получаем ответное сообщение от сервера
response = client_socket.recv(1024).decode()

print(response)

# закрываем соединение с сервером
client_socket.close()
