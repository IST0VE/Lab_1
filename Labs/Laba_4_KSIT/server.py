import socket

# создаем объект сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# определяем хост и порт
host = '127.0.0.1'
port = 12345

# связываем объект сокета с хостом и портом
server_socket.bind((host, port))

# слушаем входящие соединения
server_socket.listen(1)

print('Сервер запущен и готов к работе')

while True:
    # принимаем входящее соединение
    client_socket, addr = server_socket.accept()
    
    # получаем сообщение от клиента
    message = client_socket.recv(1024).decode()
    
    # переворачиваем сообщение
    message_reversed = message[::-1]
    
    # переводим сообщение в верхний регистр
    message_upper = message.upper()
    
    # определяем количество символов в сообщении
    message_length = len(message)
    
    # генерируем дополнительную информацию
    additional_info = 'Сервер получил сообщение и обработал его'
    
    # формируем ответное сообщение
    response = f'Сообщение: {message}\nПеревернутое сообщение: {message_reversed}\nСообщение в верхнем регистре: {message_upper}\nКоличество символов: {message_length}\n{additional_info}'
    
    # отправляем ответное сообщение клиенту
    client_socket.send(response.encode())
    
    # закрываем соединение с клиентом
    client_socket.close()
