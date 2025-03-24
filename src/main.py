import time
import threading
from modules.eye_blink import track_eye_blinks  # Update if function name differs
from modules.posture_detection import track_posture  # Update if function name differs
from modules.disengagement import track_activity  # Update if function name differs

def analyze_data():
    """Collects and analyzes data every hour"""
    while True:
        time.sleep(3600)  # Wait for 1 hour
        print("\n Analyzing Data...")

        # Here, you can read the results of eye blinks, posture, and disengagement.
        print(" Eye Blink Data Analyzed")
        print(" Posture Data Analyzed")
        print(" Disengagement Data Analyzed")
        print("\n Report Generated!")

if __name__ == "__main__":
    print(" Starting Monitoring System...")

    # Create threads for each feature
    eye_thread = threading.Thread(target=track_eye_blinks, daemon=True)
    posture_thread = threading.Thread(target=track_posture, daemon=True)
    disengagement_thread = threading.Thread(target=track_activity, daemon=True)
    analysis_thread = threading.Thread(target=analyze_data, daemon=True)

    # Start all threads
    eye_thread.start()
    posture_thread.start()
    disengagement_thread.start()
    analysis_thread.start()

    # Keep the main program running
    while True:
        time.sleep(1)  # Prevents the main script from exiting
