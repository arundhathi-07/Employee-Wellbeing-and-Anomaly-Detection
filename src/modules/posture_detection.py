import cv2
import mediapipe as mp
import time

class PostureTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.bad_posture_count = 0
        self.good_posture_count = 0
        self.last_print_time = time.time()

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        posture_status = "No Posture Data"
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
            hip_y = (landmarks[23].y + landmarks[24].y) / 2
            nose_y = landmarks[0].y
            
            is_slouching = shoulder_y > hip_y
            is_leaning_forward = nose_y < shoulder_y - 0.05
            
            if is_slouching or is_leaning_forward:
                self.bad_posture_count += 1
                posture_status = "Bad Posture"
                print("[POSTURE] Bad posture detected!")
            else:
                self.good_posture_count += 1
                posture_status = "Good Posture"
            
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
        # Print status every 5 seconds
        if time.time() - self.last_print_time > 5:
            print(f"[POSTURE] Good posture count: {self.good_posture_count} | Bad posture count: {self.bad_posture_count}")
            self.last_print_time = time.time()
        
        return frame, posture_status