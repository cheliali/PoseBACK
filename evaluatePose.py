import cv2
import mediapipe as mp
import numpy as np
import json
import math

mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose 

with open('body_poses_model.json', 'rb') as f:
    model = json.load(f)

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def calculate_distance(x1, y1, x2, y2):
    dist=math.sqrt((x2-x1)**2+(y2-y1)**2)

    return dist

def evaluatePose(frame, posename, calificacionref):
    try:
        currentAngles = getCurrentAngles(frame)
        calificacionesIndividuales=[]
        sumatoria=0

        for angleName in model["poses"][posename].keys():
            powerval=int(model["poses"][posename][angleName] - currentAngles[angleName])**2
            squareval=math.sqrt(powerval)

            for calificacion in model["calificacion"].keys():
                if (squareval in range(model["calificacion"][calificacion][0],model["calificacion"][calificacion][1])):
                    calificacionesIndividuales.append({"name":angleName, "calificacion":calificacion})
                    sumatoria=sumatoria+int(calificacion)
                
        promedio=sumatoria/len(calificacionesIndividuales)

        if (int(promedio)>calificacionref):
            cv2.imwrite("frame.jpg", frame)
            calificacionref=int(promedio)
        return calificacionesIndividuales
    
    except:
        return []
                    
def getCurrentAngles(frame):
    with mp_pose.Pose(
        static_image_mode=True) as pose:
        
        results=pose.process(frame)
        try:
            landmarks=results.pose_landmarks.landmark
            
            landmarksCoords={}
            for landMark in model["landmarks"]:
                landmarksCoords[landMark.lower()]=[landmarks[mp_pose.PoseLandmark[landMark].value].x,landmarks[mp_pose.PoseLandmark[landMark].value].y]

            # refdistance=calculate_distance(right_hip[], right_hip[], , ,)
            # distance=calculate_distance(right_knee[0],right_knee[1],left_knee[0],left_knee[1])

            #Obtener angulos
            angulos = model["angulos"]
            currentAngles = {}
            for anguloKey in angulos:
                currentAngles[anguloKey] = calculate_angle(landmarksCoords[angulos[anguloKey][0]],landmarksCoords[angulos[anguloKey][1]],landmarksCoords[angulos[anguloKey][2]])          
            return currentAngles

        except:
            pass

        if results.pose_landmarks is not None:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                mp_drawing.DrawingSpec(color=(128,0,250), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
                )
