import RPi.GPIO as GPIO
import time

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

global motors
motors={
    "x":{
        "pins":[8,10,12,16],
         "forward":True,
         "on":False,
         "maxSteps":450,
         "currentSteps":0
        },
    "z":{
        "pins":[26,24,22,18],
         "forward":True,
         "on":False,
         "maxSteps":1000,
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

def interruptX(channel):
    global motors
    motors["x"]["forward"]=False
    motors['x']['on'] = False

def interruptZ(channel):
    global motors
    motors["z"]["forward"]=False
    motors['z']['on'] = False
    
def apagar(axis):
    global motors
    motors[axis]['on'] = False
    for pin in motors[axis]["pins"]:
        GPIO.output(pin, 0)


GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(35, GPIO.FALLING,
                      callback=interruptZ,
                      bouncetime=100)

GPIO.add_event_detect(36, GPIO.FALLING,
                      callback=interruptX,
                      bouncetime=100)

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
        
def move(axis, forward):
    global motors
    motors[axis]['on'] = True
    try:
        while (motors[axis]['on']):
            if forward:
                moveMotor(seq,axis)
                motors[axis]["currentSteps"]-=1
            else:
                moveMotor(seq2,axis)
                motors[axis]["currentSteps"]+=1
                    
            if (motors[axis]["currentSteps"]==motors[axis]["maxSteps"]):
                apagar(axis)
                print("llego al limite")
            
        apagar(axis)
    
    except KeyboardInterrupt: 
        GPIO.cleanup()

apagar('x')
apagar('z')
