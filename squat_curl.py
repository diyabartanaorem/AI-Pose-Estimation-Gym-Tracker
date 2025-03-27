import cv2
import mediapipe as mp
import numpy as np
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


cap = cv2.VideoCapture(0)

left_counter = 0
right_counter = 0
left_stage = None
right_stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret,frame = cap.read()

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
            # Get left upper body coordinates
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y ]
            
            # Get left lower body coordinates
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y ]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y ]

            # Calculate upper body angle
            left_upper_angle = calculate_angle(left_shoulder,left_hip,left_knee)
            left_lower_angle = calculate_angle(left_hip,left_knee,left_ankle)


            # Visualize
            cv2.putText(image,str(left_upper_angle),
                        tuple(np.multiply(left_hip,[640,480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2, cv2.LINE_AA)
            
            cv2.putText(image,str(left_lower_angle),
                        tuple(np.multiply(left_knee,[640,480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2, cv2.LINE_AA)
            
            # Squat left_counter logic
            if left_lower_angle < 135:
                left_stage = "down"
            if left_lower_angle > 160 and left_stage=="down"  :   #and left_upper_angle>90 and left_upper_angle<130
                left_stage ="up"
                left_counter += 1
                print(left_counter)


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


        
        mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(247,117,66), thickness=2 , circle_radius=2),
                                 mp_drawing.DrawingSpec(color=(247,66,230), thickness=2 , circle_radius=2)
                                 )
        
        cv2.imshow('Mediapipe Feed',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()