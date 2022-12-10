import cv2 as cv
import tensorflow as tf
import numpy as np
import pandas as pd
import time
import math
import mediapipe as mp



palm = [0,5,9,13,17]
def midpoint(lmlist):
    nl_x = []
    nl_y = []
    for i, x, y in lmlist:
        if i in palm:
            nl_x.append(x)
            nl_y.append(y)
    newx = sum(nl_x)//len(nl_x)
    newy = (sum(nl_y)//len(nl_y))
    return newx,newy

class hand_recognizer():
    def __init__(self, mode = False, num_hands=1, detection_confidence = 0.5, tracking_confidence = 0.5, model_complexity = 1):
        self.model_complexity = model_complexity
        self.mode = mode
        self.num_hands = num_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.num_hands, self.model_complexity, self.detection_confidence, self.tracking_confidence)
        self.draw = mp.solutions.drawing_utils

    def identifier(self,img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 3, (255, 0, 255), cv.FILLED)
        return lmlist

def run(cap, detector):
    cap = cv.VideoCapture(0)
    detector = hand_recognizer()
    while True:
        success, img = cap.read()
        img = detector.identifier(cv.flip(img,1))
        lmlist = detector.findPosition(cv.flip(img,1))
        if len(lmlist) != 0:
    #         print(lmlist[0])
            x,y = midpoint(lmlist)
            yield x,y
#             print(x,y)
#             print("x->"+str(x)+" y->"+str(y))
        if cv.waitKey(1) & 0xFF==ord('q'):
            break
        cv.imshow("Image", img)
        cv.waitKey(1)
    cap.release()
    cv.destroyAllWindows()



cap = cv.VideoCapture(0)
detector = hand_recognizer()
for val in run(cv.VideoCapture(0), hand_recognizer()):
    print(val)
