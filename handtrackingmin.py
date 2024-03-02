import cv2 
import mediapipe as mp 
import time 

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # Camera doesn't show without this: https://forum.opencv.org/t/videoio-v4l2-dev-video0-select-timeout/8822/5

# Mediapipe 
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

previousTime = 0
currentTime = 0

while True:
    success, img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks: # If there are hands detected 
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape # Height, width, channels 
                cx, cy = int(lm.x*w), int(lm.y*h)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # Draw lines connecting hand landmarks
    
    
    # Displaying FPS
    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)