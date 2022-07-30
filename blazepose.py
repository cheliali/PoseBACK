import cv2
import os
from flask import Flask
from evaluatePose import evaluateVideo

name="out.mp4"

def iniciar(id,pose):
    global userid, posename
    userid = id
    posename = pose
    return
    
def videostart(cap):
    global show
    show=True
    cap.set(cv2.CAP_PROP_FPS,30)
    outmp4 = cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'mp4v'), 30, (640,480))
    while (show):
        ret, frame = cap.read()
        if ret:
            outmp4.write(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
        else:
            break
    cap.release()
    outmp4.release()
    cv2.destroyAllWindows()

def terminar():
    global show
    show=False
    return

def evaluate():
    global posename
    finalGrade = evaluateVideo(posename)
    print("final: ", finalGrade)
    return finalGrade