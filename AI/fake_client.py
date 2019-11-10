import json
import socket

while True:
    text = input("?")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8005
    s.connect((host, port))
    s.send(text.encode('utf-8'))
    message = s.recv(1024)
    s.close()
    print(message)