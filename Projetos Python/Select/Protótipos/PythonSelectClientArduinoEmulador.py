import socket
import sys

server_address = ('localhost', 65432)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
sock.connect(server_address)

while 1:
    message = input("Teste: ").encode()
    print("Enviando para {} a mensagem {}".format(sock.getsockname(), message))
    sock.sendall(message)

    data = sock.recv(1024)
    print("{}: recebido {}".format(sock.getsockname(), data))

    if not data:          
        print("Fechando {}".format(sock.getsockname()))
        sock.close()
    

