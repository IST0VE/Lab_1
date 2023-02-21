import socket
import time

host = 'localhost'  # IP address of the server
port = 20001         # Port number to listen on

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    # Request the current time from the server
    message = "Show time".encode()
    client.sendto(message, (host, port))

    # Receive the current time from the server
    data, address = client.recvfrom(1024)
    received_time = data.decode()

    print("The current time is:", received_time)
