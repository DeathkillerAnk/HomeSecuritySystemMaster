import os
from random import shuffle
from sklearn import svm
import pickle
import numpy as np
import pandas as pd
from os import walk
import json
from sklearn.externals import joblib


def train():
    namesJson = []

    with open("data/lastEncodingSave.json") as data_file:
        namesJson = json.load(data_file)

    data = []

    labels = list(namesJson.keys())

    for i in labels:
        for j in os.listdir(i):
            temp = [i]
            temp.extend(np.load("data"+"/"+i+'/'+j).tolist())
            data.append(temp)

    shuffle(data)

    yList = []

    for i, d in enumerate(data):
        yList.append(data[i].pop(0))

    X = np.array(data)
    y = np.array(yList)


    clf = svm.SVC(C=1, kernel='linear', probability=True)
    clf.fit(X, y.ravel())

    fName = "classifier.pkl"
    joblib.dump(clf, fName)