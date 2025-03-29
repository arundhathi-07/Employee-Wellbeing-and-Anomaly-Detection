import dlib
import os
import cv2
from scipy.spatial import distance
import time

# Dynamically locate the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "shape_predictor_68_face_landmarks (2).dat")

# Check if model file exists before loading
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"[ERROR] Model file not found: {MODEL_PATH}")


class EyeBlinkTracker:
    def __init__(self):
        print("[INFO] Initializing Eye Blink Tracker...")
        
        # Initialize face detector and shape predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(MODEL_PATH)
        
        self.blink_count = 0
        self.eye_closed = False
        self.last_print_time = time.time()

    def eye_aspect_ratio(self, landmarks, eye_points):
        """Calculates Eye Aspect Ratio (EAR) to detect blinks."""
        p1, p2, p3, p4, p5, p6 = [landmarks.part(i) for i in eye_points]
        
        # Calculate vertical and horizontal distances
        vertical_dist = (
            distance.euclidean((p2.x, p2.y), (p6.x, p6.y)) +
            distance.euclidean((p3.x, p3.y), (p5.x, p5.y))
        ) / 2
        horizontal_dist = distance.euclidean((p1.x, p1.y), (p4.x, p4.y))
        
        return vertical_dist / horizontal_dist

    def process_frame(self, frame,gray):
        """Processes a frame and detects blinks."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        for face in faces:
            landmarks = self.predictor(gray, face)

            left_eye = (36, 37, 38, 39, 40, 41)
            right_eye = (42, 43, 44, 45, 46, 47)

            avg_ratio = (
                self.eye_aspect_ratio(landmarks, left_eye) +
                self.eye_aspect_ratio(landmarks, right_eye)
            ) / 2

            # Detect blink based on EAR threshold
            if avg_ratio < 0.2:
                if not self.eye_closed:
                    self.blink_count += 1
                    self.eye_closed = True
                    print(f"[EYE] Blink detected! Total blinks: {self.blink_count}")
            else:
                self.eye_closed = False

        # Print blink status every 5 seconds
        if time.time() - self.last_print_time > 5:
            print(f"[INFO] Blinks so far: {self.blink_count}")
            self.last_print_time = time.time()

        return frame, self.blink_count
