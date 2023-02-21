import socket
import time

# Создание сокета UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Привязка сокета к адресу и порту
sock.bind(('localhost', 20001))
print("Ожидание подключения клиента...")

while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('utf-8')
    print("Клиент {} подключился".format(addr))
    name, addr = addr
    # Отправка сообщения клиенту каждые 3 секунды
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        message = f"{name} {current_time}"
        sock.sendto(message.encode('utf-8'), (str(addr), 20001))
        time.sleep(3)
