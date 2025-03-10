import dlib
import cv2
from scipy.spatial import distance

def track_eye_blinks():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("src/models/shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0)
    blink_count = 0
    eye_closed = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            def eye_aspect_ratio(landmarks, eye_points):
                p1, p2, p3, p4, p5, p6 = [landmarks.part(i) for i in eye_points]
                vertical_dist = (distance.euclidean((p2.x, p2.y), (p6.x, p6.y)) +
                                 distance.euclidean((p3.x, p3.y), (p5.x, p5.y))) / 2
                horizontal_dist = distance.euclidean((p1.x, p1.y), (p4.x, p4.y))
                return vertical_dist / horizontal_dist

            left_eye = (36, 37, 38, 39, 40, 41)
            right_eye = (42, 43, 44, 45, 46, 47)
            avg_ratio = (eye_aspect_ratio(landmarks, left_eye) + eye_aspect_ratio(landmarks, right_eye)) / 2

            if avg_ratio < 0.2:
                if not eye_closed:
                    blink_count += 1
                    eye_closed = True
                    print(f"Blink detected! Total blinks: {blink_count}")
            else:
                eye_closed = False

        cv2.putText(frame, f"Blinks: {blink_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Eye Blink Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
