import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global variable to store rep data
left_rep_data = {"left_counter": 0, "left_stage": None}

def get_reps():
    return left_rep_data

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

def process_video(cap):
    global left_rep_data    
    left_counter = 0
    left_stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                # Calculate angle
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

                # Squat counter logic
                if left_knee_angle < 135:
                    left_stage = "Down"
                if left_knee_angle > 160 and left_stage == "Down":
                    left_stage = "Up"
                    left_counter += 1
                left_rep_data["left_counter"] = left_counter
                left_rep_data["left_stage"] = left_stage                    

                # Visualize angle and counter
                cv2.putText(image, str(int(left_knee_angle)),
                            tuple(np.multiply(left_knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # cv2.rectangle(image, (0, 0), (250, 75), (245, 117, 16), -1)
                # cv2.putText(image, 'REPS', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.putText(image, str(left_counter), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                # cv2.putText(image, 'STAGE', (85, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.putText(image, left_stage if left_stage else '-', (80, 70),
                #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Render landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(247,117,66), thickness=2 , circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(247,66,230), thickness=2 , circle_radius=2)
                                    )   
            # Stream to Flask
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
