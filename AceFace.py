import cv2
import sys
import numpy as np


cascPath = sys.argv[1]
imagedb = sys.argv[2]

faceCascade = cv2.CascadeClassifier(cascPath)

recognizer = cv2.createLBPHFaceRecognizer()

vidcap = cv2.VideoCapture('Compton.mp4')
