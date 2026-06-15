import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import threading

class HandDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options, 
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None
        self.lock = threading.Lock()

    def process_frame(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        with self.lock:
            timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
            self.results = self.detector.detect_for_video(mp_image, timestamp)
        
        if self.results and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                h, w, _ = img.shape
                # Manual connection list for drawing lines
                connections = [(0,1), (1,2), (2,3), (3,4), (0,5), (5,6), (6,7), (7,8), (5,9), (9,10), (10,11), (11,12), (9,13), (13,14), (14,15), (15,16), (13,17), (0,17), (17,18), (18,19), (19,20)]
                for s, e in connections:
                    pt1 = (int(hand_landmarks[s].x * w), int(hand_landmarks[s].y * h))
                    pt2 = (int(hand_landmarks[e].x * w), int(hand_landmarks[e].y * h))
                    cv2.line(img, pt1, pt2, (0, 255, 0), 2)
                for lm in hand_landmarks:
                    cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 5, (255, 0, 0), cv2.FILLED)
        return img

    def getLandmarks(self):
        if self.results and self.results.hand_landmarks:
            return self.results.hand_landmarks[0]
        return None