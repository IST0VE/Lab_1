import socket

# IP-адрес и порт сервера, к которому мы подключаемся
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Запрос ввода сообщения от пользователя
message = input("Enter a message: ")

# Создание сокета для протокола UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправка сообщения серверу по заданному IP-адресу и порту
sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

# Вывод сообщения о подключении к серверу
print("Connected to server.")

# Получение ответа от сервера и адреса отправителя
data, addr = sock.recvfrom(1024)
# Декодирование ответа в строку
response = data.decode()
# Вывод ответа на экран
print(response)
sock.close()
