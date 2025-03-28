import dlib
import cv2
from scipy.spatial import distance
import time

class EyeBlinkTracker:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
        self.blink_count = 0
        self.eye_closed = False
        self.last_print_time = time.time()

    def eye_aspect_ratio(self, landmarks, eye_points):
        p1, p2, p3, p4, p5, p6 = [landmarks.part(i) for i in eye_points]
        vertical_dist = (distance.euclidean((p2.x, p2.y), (p6.x, p6.y)) +
                        distance.euclidean((p3.x, p3.y), (p5.x, p5.y))) / 2
        horizontal_dist = distance.euclidean((p1.x, p1.y), (p4.x, p4.y))
        return vertical_dist / horizontal_dist

    def process_frame(self, frame, gray):
        faces = self.detector(gray)
        for face in faces:
            landmarks = self.predictor(gray, face)
            
            left_eye = (36, 37, 38, 39, 40, 41)
            right_eye = (42, 43, 44, 45, 46, 47)
            avg_ratio = (self.eye_aspect_ratio(landmarks, left_eye) + 
                        self.eye_aspect_ratio(landmarks, right_eye)) / 2
            
            if avg_ratio < 0.2:
                if not self.eye_closed:
                    self.blink_count += 1
                    self.eye_closed = True
                    print(f"[EYE] Blink detected! Total blinks: {self.blink_count}")
            else:
                self.eye_closed = False
        
        # Print status every 5 seconds
        if time.time() - self.last_print_time > 5:
            print(f"[EYE] Current blink count: {self.blink_count}")
            self.last_print_time = time.time()
        
        return frame, self.blink_count