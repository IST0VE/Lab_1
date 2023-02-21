import socket

# IP-адрес и порт для прослушивания
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Создание сокета для протокола UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязка сокета к заданному IP-адресу и порту
sock.bind((UDP_IP, UDP_PORT))

# Вывод сообщения о начале ожидания подключения клиента
print("Waiting for client connection...")

# Бесконечный цикл для прослушивания входящих сообщений
while True:
    # Получение данных и адреса отправителя
    data, addr = sock.recvfrom(1024)
    # Декодирование полученных данных в строку
    message = data.decode()
    # Инвертирование строки (переворачивание)
    reversed_message = message[::-1]
    # Преобразование строки к верхнему регистру
    upper_case_message = message.upper()
    # Вычисление длины строки
    message_length = str(len(message))
    # Формирование ответа
    response = f"Client message: {message}\nReversed message: {reversed_message}\nUppercase message: {upper_case_message}\nMessage length: {message_length}"
    # Отправка ответа обратно клиенту
    sock.sendto(response.encode(), addr)
    # Вывод сообщения о подключении клиента
    print(f"Client {addr} connected.")
    break
sock.close()

