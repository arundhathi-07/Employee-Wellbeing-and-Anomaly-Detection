import cv2
import threading
from modules.eye_blink import EyeBlinkTracker
from modules.posture_detection import PostureTracker
from modules.disengagement import DisengagementTracker

def main():
    # Initialize trackers
    eye_tracker = EyeBlinkTracker()
    posture_tracker = PostureTracker()
    disengagement_tracker = DisengagementTracker(timeout=15)
    
    # Start disengagement tracker in background
    disengagement_tracker.start()
    
    # Open video capture
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame through all trackers
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Eye blink detection
        frame, blink_count = eye_tracker.process_frame(frame, gray)
        
        # Posture detection
        frame, posture_status = posture_tracker.process_frame(frame)
        
        # Display information
        cv2.putText(frame, f"Blinks: {blink_count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Posture: {posture_status}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                    (0, 0, 255) if posture_status == "Bad Posture" else (0, 255, 0), 2)
        cv2.putText(frame, f"Engagement: {'Disengaged' if disengagement_tracker.disengaged else 'Engaged'}", 
                    (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255) if disengagement_tracker.disengaged else (0, 255, 0), 2)
        
        cv2.imshow("Combined Tracking System", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    disengagement_tracker.stop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()