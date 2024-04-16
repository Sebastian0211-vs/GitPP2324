from __future__ import print_function
import cv2
import sys

import argparse

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# Use IP camera
video_capture = cv2.VideoCapture("rtsp://172.16.1.50:554/user=admin_password=EptmPP1950_channel=1_stream=0.sdp")

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)