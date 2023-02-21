import socket

# создаем объект сокета для UDP-протокола
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# задаем адрес и порт сервера
server_address = ('localhost', 20001)

# получаем имя клиента
name = input('Введите ваше имя: ')

# отправляем имя на сервер для регистрации
sock.sendto(name.encode(), server_address)

# выводим сообщение об успешном подключении
print('Подключение к серверу выполнено.')

while True:
    # получаем сообщение от сервера и выводим его на экран
    data, server = sock.recvfrom(4096)
    message = data.decode()
    print(message)
