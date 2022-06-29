import cv2
import os
from flask import Flask
from evaluatePose import evaluatePose


def iniciar(id,pose,calif):
    global userid, posename, calificacionref
    userid = id
    posename = pose
    calificacionref = calif
    return
    
def videostart(cap):
    global show
    show=True
    while (show):
        ret, frame = cap.read()
        if ret:
            calificacionfin= evaluatePose(frame, posename, calificacionref)
            print(calificacionfin)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def terminar():
    global show
    show=False
    return
    
 

