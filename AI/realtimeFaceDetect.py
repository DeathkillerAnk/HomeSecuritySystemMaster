import sys
import dlib
from skimage import io
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from PIL import Image
import json
import sys
import dlib
import cv2
import openface
import os
from sklearn.externals import joblib

import networkServer
from networkServer import States

import networkClient as nClient

import _thread

try:
    _thread.start_new_thread(networkServer.rpcServer, ())
    print("yo")
except Exception as e:
    print("error in rpc thread")
    logger.error(e, exc_info=True)

predictor_model = "models/shape_predictor_68_face_landmarks.dat"
face_recognition_model = 'models/dlib_face_recognition_resnet_model_v1.dat'
fName = "classifier.pkl"

#webcam number
cap = cv2.VideoCapture(0)
face_detector = dlib.get_frontal_face_detector()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_aligner = openface.AlignDlib(predictor_model)

# face_name = "Adnan Sayed"
saveCountReset = False

outOfRecording = 40
count = 0

saveImgLoc = "../untitled/Image"


def saveCapturedImg(image):
    im = Image.fromarray(image)

    with open("data/configs.json") as df:
        data = json.load(df)

    data["lastImageNumber"] += 1

    imageName = data["lastImageNumber"] + ".png"
    im.save(saveImgLoc+"/"+imageName)

    with open("data/configs.json", 'w') as data_file:
        json.dump(data, data_file)

    return imageName


def saveEncoding(faceName, encoding):
    global count

    with open('data/lastEncodingSave.json') as data_file:
        data = json.load(data_file)

        try:
            data[faceName]
        except KeyError:
            data[faceName] = 0

        if not os.path.exists(faceName):
            os.makedirs(faceName)

        np.save("data" + "/" + faceName + "/" + "encoding" + str(data[faceName]), np.array(encoding))

        data[faceName] += 1
        count += 1

        nClient.sendMessageToServer({"rpc": "updateRecordingStatus", "args": [count, outOfRecording]})

        print(data[faceName])

        with open('lastEncodingSave.json', 'w') as df:
            json.dump(data, df)


clf = joblib.load(fName)


def predictEncoding(encoding):
    result = clf.predict([encoding])
    print(clf.decision_function([encoding]))
    print(result)
    return result[0]


print("starting face detect")
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = frame

    detected_faces = face_detector(gray, 1)
    # print("I found {} faces ".format(len(detected_faces)))

    showImg = np.copy(gray)
    # for i, face_rect in enumerate(detected_faces):
    #     cv2.rectangle(showImg, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), (0,0,0), 3)
    #
    #     pose_landmarks = face_pose_predictor(gray, face_rect)
    #     alignedFace = face_aligner.align(534, gray, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    #     cv2.imshow('aligned', alignedFace)


    if len(detected_faces) > 0:
        face_rect = detected_faces[0]
        cv2.rectangle(showImg, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), (0, 0, 0),
                      3)

        pose_landmarks = face_pose_predictor(gray, face_rect)
        alignedFace = face_aligner.align(534, gray, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        cv2.imshow('aligned', alignedFace)

        encodings = np.array(face_encoder.compute_face_descriptor(gray, pose_landmarks, 1))

        # todo do stuff with encoding here

        if networkServer.currentState == States.predict:
            name = predictEncoding(encodings)
            capImg = saveCapturedImg(showImg)
            #capImg = "yo"
            nClient.sendMessageToServer({"rpc": "capturedFace", "args": [capImg, name]})
        if networkServer.currentState == States.recording:

            if not saveCountReset:
                count = 0
                print("starting surveillance")
            saveCountReset = True
            saveEncoding(networkServer.face_name, encodings)
        else:
            saveCountReset = False

            # break

    # Display the resulting frame
    cv2.imshow('frame2', showImg)

    button = cv2.waitKey(1) & 0xFF
    if button == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
