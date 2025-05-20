import cv2
import mediapipe as mp
import numpy as np
from playsound import playsound

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) #First point
    b = np.array(b) #Second point
    c = np.array(c) #Third point

    radian = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radian * 180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle
    return angle

def process_video(cap):
    left_counter = 0
    right_counter = 0
    left_stage = None
    right_stage = None

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret,frame = cap.read()
            if not ret:
                break            

            # Redcolor image
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark


            # left_side    
                # Get coordinates
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ]

                # Calculae angle
                left_angle = calculate_angle(left_elbow,left_shoulder,left_hip)

                # Visualize
                cv2.putText(image,str(left_angle),
                            tuple(np.multiply(left_elbow,[640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2, cv2.LINE_AA)
                # Curl left_counter logic
                if left_angle <30:
                    left_stage = "down"
                if left_angle <=90 and left_angle>80 and left_stage=="down":
                    left_stage ="up"
                    left_counter += 1
                    print(left_counter)
            

            # right_side    
                # Get coordinates
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y ]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y ]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y ]

                # Calculae angle
                right_angle = calculate_angle(right_elbow,right_shoulder,right_hip)

                # Visualize
                cv2.putText(image,str(right_angle),
                            tuple(np.multiply(right_elbow,[640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2, cv2.LINE_AA)
                # Curl right_counter logic
                if right_angle <30:
                    right_stage = "down"
                if right_angle <=90 and right_angle>80 and right_stage=="down":
                    right_stage ="up"
                    right_counter += 1
                    print(right_counter)
                

            except:
                pass

            # Render curl left_counter
            # Setup status box

            cv2.rectangle(image,(0,0),(255,73),(245,177,16),-1)

            # Repdata
            cv2.putText(image,'REPS',(15,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image,str(left_counter),(10,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)

            # Stagedata
            cv2.putText(image,'STAGE',(85,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image,left_stage,(80,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)

            
            # Render curl right_counter
            # Setup status box

            cv2.rectangle(image,(400,0),(655,73),(245,177,16),-1)

            # Repdataq
            cv2.putText(image,'REPS',(410,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image,str(right_counter),(410,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)

            # Stagedata 
            cv2.putText(image,'STAGE',(490,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image,right_stage,(480,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)

            
            mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(247,117,66), thickness=2 , circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(247,66,230), thickness=2 , circle_radius=2)
                                    )
            
            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        