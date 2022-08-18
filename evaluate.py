from time import time
import cv2
import mediapipe as mp
import numpy as np
import json
import math

from storage import createHistory

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
    dist=(math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2))*100
    return dist

def evaluateVideo(posename, userid):

    cap=cv2.VideoCapture("/home/pi/Desktop/out.mp4")
    global calificacionRef, bestIndividualGrades
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cont = 0
    calificacionRef = 0
    bestIndividualGrades=[]
    videoEnd=False
    calificacionfin = []
    while(cap.isOpened() and not videoEnd):
        ret, frame = cap.read()
        if ret:
            if(cont % 15 == 0):
                calificacionfin=evaluatePose(frame, posename) 
                print(calificacionfin)
        else:
            videoEnd=True
        cont = cont + 1
    
    createHistory(posename, userid, calificacionfin)
    return calificacionfin

def evaluatePose(frame, posename):
    global calificacionRef, bestIndividualGrades
    
    try:
        resp = getCurrentAngles(frame)
        currentAngles = resp[0]
        currentDistances = resp[1]
        calificacionesIndividuales=[]
        sumatoria=0
        distanciaref=currentDistances["distancehipknee"]  

        for angleName in model["poses"][posename].keys():
            observacion=''
            if(str(angleName).find("distance") != -1):
                finalval=currentDistances[angleName]
                finalval=(finalval*1)/distanciaref
                finalval=(model["poses"][posename][angleName] - finalval)**2
                finalval=math.sqrt(finalval)
                
            else:
                powerval=int(model["poses"][posename][angleName] - currentAngles[angleName])**2
                finalval=math.sqrt(powerval)

            calificacionModelSelector = "calificacionDistancias" if str(angleName).find("distance") != -1  else "calificacionAngulos"
            for calificacion in model[calificacionModelSelector].keys():
                if (model[calificacionModelSelector][calificacion][0] <= finalval < model[calificacionModelSelector][calificacion][1]):
                    calificacionesIndividuales.append({"name":angleName, "grade":calificacion, "improve":observacion})
                    sumatoria=sumatoria+int(calificacion)
  
        promedio=sumatoria/len(calificacionesIndividuales)
 
        if promedio>calificacionRef:          
            calificacionRef=promedio
            bestIndividualGrades=calificacionesIndividuales
            cv2.imwrite('/home/pi/Desktop/finalIm.jpg',frame)

        return bestIndividualGrades
    
    except:
        return bestIndividualGrades
                    
def getCurrentAngles(frame):
    with mp_pose.Pose(
        static_image_mode=True) as pose:
        results=pose.process(frame)
        try:
            landmarks=results.pose_landmarks.landmark
            
            landmarksCoords={}
            for landMark in model["landmarks"]:
                landmarksCoords[landMark.lower()]=[landmarks[mp_pose.PoseLandmark[landMark].value].x,landmarks[mp_pose.PoseLandmark[landMark].value].y]


            angulos = model["angulos"]
            currentAngles = {}
            currentDistances={}
            for anguloKey in angulos:        
                if(str(anguloKey).find("distance") != -1):            
                    currentDistances[anguloKey]=calculate_distance(landmarksCoords[angulos[anguloKey][0]],landmarksCoords[angulos[anguloKey][1]])
                else:            
                    currentAngles[anguloKey] = calculate_angle(landmarksCoords[angulos[anguloKey][0]],landmarksCoords[angulos[anguloKey][1]],landmarksCoords[angulos[anguloKey][2]])        

            # mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            #                     mp_drawing.DrawingSpec(color=(245,117,66), thickness=5, circle_radius=5), 
            #                     mp_drawing.DrawingSpec(color=(245,66,230), thickness=5, circle_radius=5) 
                                #  ) 
            return [currentAngles, currentDistances]            

        except:
            pass


''' history={
    "username":"hola",
    "pose":"pose",
    "calificacionesInd":"7"
}

jsonString = json.dumps(history)
jsonFile = open("/home/pi/Desktop/history.json", "w")
jsonFile.write(jsonString)
jsonFile.close() '''