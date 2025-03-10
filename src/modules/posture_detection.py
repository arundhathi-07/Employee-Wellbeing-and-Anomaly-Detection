import cv2
import mediapipe as mp
import time

def track_posture():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    bad_posture_count = 0
    good_posture_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
            hip_y = (landmarks[23].y + landmarks[24].y) / 2
            nose_y = landmarks[0].y

            is_slouching = shoulder_y > hip_y
            is_leaning_forward = nose_y < shoulder_y - 0.05

            if is_slouching or is_leaning_forward:
                bad_posture_count += 1
                posture_status = "Bad Posture"
            else:
                good_posture_count += 1
                posture_status = "Good Posture"

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.putText(frame, f"Posture: {posture_status}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if is_slouching or is_leaning_forward else (0, 255, 0), 2)

        cv2.imshow("Posture Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
