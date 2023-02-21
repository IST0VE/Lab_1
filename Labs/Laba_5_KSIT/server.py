import socket
import threading
import time

# создаем объект сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# определяем хост и порт
host = '127.0.0.1'
port = 12345

# связываем объект сокета с хостом и портом
server_socket.bind((host, port))

# слушаем входящие соединения
server_socket.listen(2)

print('Сервер запущен и готов к работе')

# список клиентов
clients = []

# функция для обработки клиентских запросов
def handle_client(client_socket, client_address, client_name):
    print(f'Подключился клиент {client_name} ({client_address[0]}:{client_address[1]})')
    
    while True:
        try:
            # получаем сообщение от клиента
            message = client_socket.recv(1024).decode()
            
            if message == 'time':
                # отправляем текущее время клиенту
                current_time = time.strftime('%H:%M:%S', time.localtime())
                response = f'Текущее время: {current_time}'
                client_socket.send(response.encode())
            else:
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
        except:
            print(f'Клиент {client_name} ({client_address[0]}:{client_address[1]}) отключился')
            clients.remove((client_socket, client_address, client_name))
            client_socket.close()
            break

# функция для приема клиентских подключений
def accept_clients():
    while True:
        # принимаем входящее соединение
        client_socket, addr = server_socket.accept()

        # получаем имя клиента
        client_name = client_socket.recv(1024).decode()

        # добавляем клиента в список
        clients.append((client_socket, addr, client_name))

        # создаем отдельный поток для обработки клиентских запросов
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_name))
        client_thread.start()

# запускаем функцию для приема клиентских подключений
