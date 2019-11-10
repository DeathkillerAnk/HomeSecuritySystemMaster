import socket
import json
import trainEncodings
import shutil
import networkClient as nClient
from enum import Enum

s = socket.socket()
host = socket.gethostname()
port = 8005
s.bind((host, port))

States = Enum('States', 'none recording predict')

currentState = States.none
face_name = "Adam Saudagar"


def deleteCapturedData(name):

    try:
        shutil.rmtree(name)

        with open('lastEncodingSave.json') as data_file:
            data = json.loads(data_file)

        data.pop(name)

        with open('lastEncodingSave.json', 'w') as data_file:
            data_file.write(data)

    except FileNotFoundError:
        return 0

    return 1


def rpcServer():
    global currentState, face_name

    while True:
        print("rpc server listening")

        s.listen(1)
        c, addr = s.accept()
        message = c.recv(1024).decode("utf-8")

        # print('Got connection from', addr)
        #  c.send('Thank you for connecting')

        # TODO DO RPC

        dict = json.loads(message)

        response = '{"success":1}'

        if dict["rpc"] == "startLearning":
            currentState = States.none

            print("starting learning")
            trainEncodings.train()

        elif dict["rpc"] == "startRecording":
            currentState = States.recording
            face_name = dict["args"][0]
            nClient.sendMessageToServer({"rpc": "learningFinished"})
        elif dict["rpc"] == "deleteCapturedData":
            success = deleteCapturedData(dict["args"][0])
            responseDict = {"success": success}
            response = json.dumps(responseDict)
        elif dict["rpc"] == "startSurveillance":
            currentState = States.predict

        c.send(response.encode('utf-8'))
        c.close()

        # print(message)
