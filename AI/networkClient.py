import socket
import json


def sendMessageToServer(dictMessage, port=12345):
    print("sending response: ", json.dumps(dictMessage))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect((host, port))
    s.send(json.dumps(dictMessage).encode('utf-8'))
    message = s.recv(1024)
    s.close()
    print(message)
