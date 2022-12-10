from django.shortcuts import render
from Identification import hand_recognizer, midpoint, run
import cv2 as cv

cap = cv.VideoCapture(0)
detector = hand_recognizer()

def button(request):
    return render(request,'home.html')


def output(request):
    a = run(cap,detector)
    print(a)
    return render(request,'home.html',{"data":a})
