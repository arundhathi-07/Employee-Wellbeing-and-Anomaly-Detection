import cv2
import time
import threading
import streamlit as st
from datetime import datetime, timedelta
from modules.eye_blink import EyeBlinkTracker
from modules.posture_detection import PostureTracker
from modules.disengagement import DisengagementTracker

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title("Real-time Activity Monitoring System")

# Initialize session state
if 'trackers' not in st.session_state:
    st.session_state.trackers = {
        'eye': EyeBlinkTracker(),
        'posture': PostureTracker(),
        'disengagement': DisengagementTracker(timeout=15)
    }
    st.session_state.disengagement_thread = None
    st.session_state.running = False
    st.session_state.last_update = 0
    st.session_state.last_engaged_time = datetime.now()
    st.session_state.show_inactive_notification = False

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    if st.button("Start Monitoring"):
        st.session_state.running = True
        st.session_state.last_engaged_time = datetime.now()
        st.session_state.show_inactive_notification = False
        st.session_state.disengagement_thread = threading.Thread(
            target=st.session_state.trackers['disengagement'].start
        )
        st.session_state.disengagement_thread.daemon = True
        st.session_state.disengagement_thread.start()
        st.success("Monitoring started!")
    
    if st.button("Stop Monitoring"):
        st.session_state.running = False
        st.session_state.trackers['disengagement'].stop()
        st.info("Monitoring stopped")
    
    st.header("Settings")
    disengagement_timeout = st.slider(
        "Disengagement timeout (seconds)",
        min_value=5,
        max_value=60,
        value=15
    )
    st.session_state.trackers['disengagement'].timeout = disengagement_timeout

# Create columns
col1, col2 = st.columns([2, 1])

# Video feed placeholder
video_placeholder = col1.empty()

# Status display
status_container = col2.container()
status_container.header("Current Status")

# Initialize metrics
eye_metric = status_container.metric("Eye Blink Count", "0")
posture_metric = status_container.metric("Posture Status", "Not Detected")
engagement_metric = status_container.metric("Engagement Status", "Not Detected")

# Notification placeholder
notification_placeholder = col2.empty()

# Log container
log_container = col2.container()
log_container.header("Activity Log")
log_messages = log_container.empty()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Main processing loop
while st.session_state.running:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture video")
        break
    
    # Process frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Eye tracking
    frame, blink_count = st.session_state.trackers['eye'].process_frame(frame, gray)
    
    # Posture tracking
    frame, posture_status = st.session_state.trackers['posture'].process_frame(frame)
    
    # Engagement tracking
    disengaged = st.session_state.trackers['disengagement'].disengaged
    
    # Update last engaged time if user is engaged
    if not disengaged:
        st.session_state.last_engaged_time = datetime.now()
        if st.session_state.show_inactive_notification:
            notification_placeholder.empty()
            st.session_state.show_inactive_notification = False
    
    # Check for prolonged inactivity (20+ seconds)
    inactive_duration = (datetime.now() - st.session_state.last_engaged_time).total_seconds()
    if disengaged and inactive_duration >= 20:
        st.session_state.show_inactive_notification = True
    
    # Show/hide notification based on state
    if st.session_state.show_inactive_notification:
        notification_placeholder.warning(
            "⚠️ You have been inactive for a long time, please stay engaged!",
            icon="⚠️"
        )
    else:
        notification_placeholder.empty()
    
    # Convert frame to RGB for Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Update video feed
    video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
    
    # Update metrics
    eye_metric.metric("Eye Blink Count", str(blink_count))
    posture_metric.metric("Posture Status", posture_status)
    engagement_status = "Disengaged" if disengaged else "Engaged"
    engagement_metric.metric("Engagement Status", engagement_status)
    
    # Update logs periodically
    if time.time() - st.session_state.last_update > 2:
        log_message = f"""
        **Last Update:** {time.strftime('%H:%M:%S')}  
        - Blinks: {blink_count}  
        - Posture: {posture_status}  
        - Engagement: {engagement_status}  
        - Inactive Duration: {int(inactive_duration)}s  
        """
        log_messages.markdown(log_message)
        st.session_state.last_update = time.time()
    
    time.sleep(0.1)

# Cleanup when stopped
if not st.session_state.running:
    if cap.isOpened():
        cap.release()
    if st.session_state.disengagement_thread is not None:
        st.session_state.trackers['disengagement'].stop()
    
    video_placeholder.info("Monitoring stopped. Press 'Start Monitoring' to begin.")
    notification_placeholder.empty()