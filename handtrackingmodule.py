import cv2 
import mediapipe as mp 
import time 
class HandDetector():
    def __init__(self, mode=False, max_hands = 1, modelComplexity=1, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence
        self.modelComplexity = modelComplexity
        
        # Mediapipe 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.modelComplexity, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        
        self.tipIDs = [4,8,12,16,20] # The tip of the fingers -> we use this to check if the tip is lower than the landmark below it (the finger is not up)
    
    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks: # If there are hands detected 
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # Draw lines connecting hand landmarks
        return img
    
    def find_position(self, img, handNumber=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                hand = self.results.multi_hand_landmarks[handNumber]
                for id, lm in enumerate(hand.landmark):
                    h,w,c = img.shape # Height, width, channels 
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # Draw lines connecting hand landmarks
        return self.lmList
    def count_fingers_up(self):
        fingers = []
        if len(self.lmList) > 0:
            # Thumb
            fingers.append(0) # No need to check for thumb, not needed for drawing
            # 4 fingers 
            for id in range(1,5):
                if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id]-3][2]: # The origin is at the upper left corner: the y position of the tip of the finger will be lower than the y position of the landmark below the tip 
                    fingers.append(1) # Finger is up
                else:
                    fingers.append(0) # Finger not up
        return fingers


    
def main():
    
    previousTime = 0
    currentTime = 0
    detector = HandDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # Camera doesn't show without this: https://forum.opencv.org/t/videoio-v4l2-dev-video0-select-timeout/8822/5
    while True:
        success, img = cap.read()
        img = detector.count_fingers_up()
        
        
        # Displaying FPS
        currentTime = time.time()
        fps = 1/(currentTime-previousTime)
        previousTime = currentTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)



    
    
if __name__ == "__main__":
    main()