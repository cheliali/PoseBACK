from time import time
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

def calculate_distance(p1, p2):
    dist=math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    return dist

def evaluateVideo(posename):

    cap=cv2.VideoCapture("out.mp4")
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    cont = 0
    calificacionRef = 0
    videoEnd=False
    calificacionfin = []
    while(cap.isOpened() and not videoEnd):
        ret, frame = cap.read()
        if ret:
            if(cont % 15 == 0):
                calificacionfin=evaluatePose(frame, posename, calificacionRef) 
                print(calificacionfin)
        else:
            videoEnd=True
        cont = cont + 1
    return calificacionfin

def evaluatePose(frame, posename, calificacionref):
    try:
        resp = getCurrentAngles(frame)
        currentAngles = resp[0]
        currentDistances = resp[1]
        calificacionesIndividuales=[]
        sumatoria=0
        for angleName in model["poses"][posename].keys():
            if(str(angleName).find("distance") != -1):
                finalval=currentDistances[angleName]*1000
            else:
                powerval=int(model["poses"][posename][angleName] - currentAngles[angleName])**2
                finalval=math.sqrt(powerval)
            
            print("finalVal: ", finalval)

            for calificacion in model["calificacion"].keys():
                print("entra")
                if (int(finalval) in range(model["calificacion"][calificacion][0],model["calificacion"][calificacion][1])):
                    print("entra 2")
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
                landMarkValue = mp_pose.PoseLandmark[landMark].value
                landmarksCoords[landMark.lower()]=[landmarks[landMarkValue].x,landmarks[landMarkValue].y]

            #Obtener angulos
            angulos = model["angulos"]
            currentAngles = {}
            currentDistances={}
            for anguloKey in angulos:        
                if(str(anguloKey).find("distance") != -1):            
                    currentDistances[anguloKey]=calculate_distance(landmarksCoords[angulos[anguloKey][0]],landmarksCoords[angulos[anguloKey][1]])
                else:            
                    currentAngles[anguloKey] = calculate_angle(landmarksCoords[angulos[anguloKey][0]],landmarksCoords[angulos[anguloKey][1]],landmarksCoords[angulos[anguloKey][2]])              
            return [currentAngles, currentDistances]

        except:
            pass

        # if results.pose_landmarks is not None:
        #     mp_drawing.draw_landmarks(
        #         frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
        #         mp_drawing.DrawingSpec(color=(128,0,250), thickness=2, circle_radius=3),
        #         mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
        #         )
