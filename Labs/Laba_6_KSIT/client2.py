import socket

server_address = ('localhost', 20001)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        name = input("Enter your name: ")
        message = name.encode('utf-8')
        s.sendto(message, server_address)
        data, address = s.recvfrom(1024)
        print("Length of your name is:", len(name))
