import socket

HOST, PORT = "localhost", 9999

# Создаем сокет и подключаемся к серверу
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    # Получаем имя клиента
    name = input("Введите ваше имя: ")
    # Отправляем сообщение с именем на сервер
    sock.sendall(name.encode('utf-8'))
    while True:
        # Получаем ответ от сервера и выводим его на экран
        data = sock.recv(1024)
        print(data.decode('utf-8'))
