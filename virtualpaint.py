
import cv2
import mediapipe as mp
import handtrackingmodule as htm
import numpy as np
import pyvirtualcam

cap = cv2.VideoCapture(0)
# Camera doesn't show without this on Linux: https://forum.opencv.org/t/videoio-v4l2-dev-video0-select-timeout/8822/5
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
detector = htm.HandDetector(detectionConfidence=0.7)
xp, yp = 0, 0
flip = True
cam_width, cam_height = cap.get(3), cap.get(4)
imgCanvas = np.zeros((int(cam_height), int(cam_width), 3), np.uint8)
drawColor = (0, 255, 0)
while True:
    with pyvirtualcam.Camera(width=int(cam_width), height=int(cam_height), fps=30, print_fps=True) as cam:
        print(f'Using virtual camera: {cam.device}')
        frame = np.zeros((int(cam.height), int(cam.width), 3), np.uint8)  # RGB
        while True:
            # 1: Import image
            success, img = cap.read()
            if flip:
                img = cv2.flip(img, 1)
            # 2: Find hand landmarks
            img = detector.find_hands(img, draw=False)
            lmList = detector.find_position(img, draw=False)
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]  # 8 is the tip of index finger
                x2, y2 = lmList[12][1:]  # 12 is the tip of middle finger
            # 3: Check which fingers are up
            fingers = detector.count_fingers_up()
            if len(fingers) > 0:

                # 4: Selection mode if two fingers are up
                if fingers[1] and fingers[2]:  # If index and middle finger
                    xp, yp = 0, 0
                    print("Selection mode")
                # 5: Drawing mode if one finger is up
                if fingers[1] and not fingers[2]:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    print("Drawing mode")
                    if xp == 0 and yp == 0:  # First time it sees finger
                        xp, yp = x1, y1
                    cv2.line(img, (xp, yp), (x1, y1), (0, 0, 0), 6)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 6)
                    xp, yp = x1, y1

                if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                    print("Erasing mode")
                    xp, yp = 0, 0

                    if xp == 0 and yp == 0:  # First time it sees finger
                        xp, yp = x1, y1
                    cv2.line(img, (xp, yp), (x1, y1), (0, 0, 0), 100)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), 100)

                    xp, yp = x1, y1

            # merging canvas and webcam image
            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, imgInv)
            img = cv2.bitwise_or(img, imgCanvas)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cam.send(img)
            cam.sleep_until_next_frame()
