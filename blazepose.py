import cv2
import matplotlib
matplotlib.use('Agg')
import mediapipe as mp

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
from sklearn.metrics import accuracy_score # Accuracy metrics 

cap = None
mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    
def videostart():
    global cap
    
    with mp_pose.Pose(
        static_image_mode=False) as pose:

        while True:
            ret, frame = cap.read()
            if ret==False:
                break
        
            # Make detection
            frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results=pose.process(frame_rgb)
            
            # Extract landmarks
            try:
                landmarks=results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle=calculate_angle(shoulder, elbow, wrist)
                
                # Visualize angle
                cv2.putText(frame, str(angle), 
                            tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                        
            except:
                pass   

            if results.pose_landmarks is not None:
                mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=(128,0,250), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
                    )

                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')

def terminar():
    global cap 
    cap.release()
