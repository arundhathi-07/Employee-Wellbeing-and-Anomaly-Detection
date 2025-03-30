import cv2
import threading
import time
import csv
import os
import datetime
import subprocess
from modules.eye_blink import EyeBlinkTracker
from modules.posture_detection import PostureTracker
from modules.disengagement import DisengagementTracker
from modules.login import authenticate_user, track_working_hours

def get_csv_filename():
    """Generates a filename based on the current date."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    data_folder = "src/data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    return os.path.join(data_folder, f"stress_data_{today}.csv")

def initialize_csv(file_path):
    """Creates the CSV file with headers if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Blink Count", "Posture Status", "Engagement Status"])

def log_data(file_path, blink_count, posture_status, engagement_status):
    """Logs stress data to the CSV file every 5 minutes."""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), blink_count, posture_status, engagement_status])

def main():
    # Authenticate user
    user = authenticate_user()
    if not user:
        return
    
    # Initialize trackers
    eye_tracker = EyeBlinkTracker()
    posture_tracker = PostureTracker()
    disengagement_tracker = DisengagementTracker(timeout=15)
    disengagement_tracker.start()
    
    # Get CSV filename and initialize
    csv_file = get_csv_filename()
    initialize_csv(csv_file)
    
    # Open video capture
    cap = cv2.VideoCapture(0)
    last_logged_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Process frame through all trackers
        frame, blink_count = eye_tracker.process_frame(frame, gray)
        frame, posture_status = posture_tracker.process_frame(frame)
        engagement_status = "Disengaged" if disengagement_tracker.disengaged else "Engaged"
        
        # Display information
        cv2.putText(frame, f"Blinks: {blink_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Posture: {posture_status}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if posture_status == "Bad Posture" else (0, 255, 0), 2)
        cv2.putText(frame, f"Engagement: {engagement_status}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if engagement_status == "Disengaged" else (0, 255, 0), 2)
        
        cv2.imshow("Combined Tracking System", frame)
        
        # Log data every 5 minutes
        if time.time() - last_logged_time >= 300:
            log_data(csv_file, blink_count, posture_status, engagement_status)
            last_logged_time = time.time()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up and analyze stress data
    disengagement_tracker.stop()
    cap.release()
    cv2.destroyAllWindows()
    
    working_hours = track_working_hours()
    print(f"Total working hours: {working_hours}")
    
    # Analyze stress data upon logout
    analyze_script = "src/modules/analyze_stress.py"
    if os.path.exists(analyze_script):
        subprocess.run(["python", analyze_script, csv_file])
    else:
        print("[ERROR] Stress analysis script not found!")

if __name__ == "__main__":
    main()
