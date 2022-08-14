import RPi.GPIO as GPIO
import time
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

global motors, frame
motors={
    "x":{
        "pins":[8,10,12,16],
         "forward":True,
         "on":False,
         "maxSteps":800,
         "currentSteps":0
        },
    "z":{
        "pins":[26,24,22,18],
         "forward":True,
         "on":False,
         "maxSteps":5500,
         "currentSteps":0
        }
    }

seq=[[1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]]
    
seq2=[[1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,1]]

def visibility():
    global frame
    # cap= cv2.VideoCapture(0)
    # ret, frame=cap.read()
    toes=0
    nose=0
    try:
        with mp_pose.Pose(
            static_image_mode=True) as pose:
            
            results=pose.process(frame)
            landmarks=results.pose_landmarks.landmark
            # print(landmarks)

            completeNose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            completeRToe = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            completeLToe = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            
            if(0.05 < completeNose.y < 0.95):
                nose=completeNose.visibility
            if(0.05 < completeRToe.y < 0.95):
                toeRight=completeRToe.visibility
            if(0.05 < completeLToe.y < 0.95):
                toeLeft=completeLToe.visibility

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=5, circle_radius=5), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=5, circle_radius=5) 
                                ) 
            # print("DRAWING PASA")
            # cv2.imwrite('/home/pi/Desktop/test.jpeg', frame)

            toes = (toeRight + toeLeft) / 2

    except Exception as e:
        print("Hubo un error")
        print(str(e))
        pass
    return [nose, toes]

def interruptX(channel):
    global motors
    motors["x"]["forward"]=False
    motors['x']['on'] = False

def interruptZ(channel):
    global motors
    motors["z"]["forward"]=False
    motors['z']['on'] = False

GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(35, GPIO.FALLING,
                      callback=interruptZ,
                      bouncetime=100)

GPIO.add_event_detect(36, GPIO.FALLING,
                      callback=interruptX,
                      bouncetime=100)

def apagar(axis):
    global motors
    motors[axis]['on'] = False
    for pin in motors[axis]["pins"]:
        GPIO.output(pin, 0)

def moveMotor(sequence, axis):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(motors[axis]["pins"][pin], sequence[halfstep][pin])
        time.sleep(0.001)

def homing(axis, backSteps):
    global motors
    contadorm1=0
    try:
        while (contadorm1<backSteps):
            if motors[axis]["forward"]:
                moveMotor(seq,axis)
            else:
                moveMotor(seq2,axis)
                contadorm1+=1
                    
            if (contadorm1==backSteps):
                apagar(axis)
                motors[axis]["currentSteps"] = contadorm1
                print("fin del homing")
            
        apagar(axis)
    
    except KeyboardInterrupt: 
        GPIO.cleanup()
        
def move(axis, stepsBetweenVerif):
    global motors
    motors[axis]['on'] = True
    visNose, visToes=visibility()
    print(visNose)
    print(visToes)
    contSteps = 0
    try:
        # while (motors[axis]['on'] and visNariz>=0.9):
        while (((visToes < 0.9 and axis == 'x') 
                or 
                (visNose < 0.9 and axis == 'z')) 
                and motors[axis]["currentSteps"] < motors[axis]['maxSteps']):
            if(contSteps == stepsBetweenVerif):
                visNose, visToes=visibility()
                contSteps = 0
                print(visNose)
                print(visToes)
            moveMotor(seq2,axis)
            motors[axis]["currentSteps"]+=1
            # print("====== CURRENTSTEPS =======", motors[axis]["currentSteps"])
            contSteps+=1
        
        apagar(axis)

        # if(axis == 'x' and visToes < 0.9):
        #     return 'alejese por favor'
        if(axis == 'z' and (visToes < 0.9 or visNose < 0.9)):
            return 'alejese por favor'
        else:
            return 'ok'

    except KeyboardInterrupt: 
        GPIO.cleanup()

def focus():
    print("ENTRA FUNCION")
    move('x', 50)
    resp = move('z', 500)
    return resp

def setFrame(currFrame):
    global frame
    frame = currFrame

homing('x',128)
homing('z',512)
# visibility()