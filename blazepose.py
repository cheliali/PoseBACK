import cv2
from evaluate import evaluateVideo
from motores import focus, setFrame

name="/home/pi/Desktop/out.mp4"

global show, focussing, currentFrame
show = True
focussing = True

def iniciar(id,pose):
    global userid, posename, focussing, show
    userid = id
    posename = pose
    # print("INICIAR FOCUSSING")
    resp = focus()
    focussing=False
    return resp
    
def videostart(cap):
    global show, focussing
    # print('======= FOCUSING INICIO ========', focussing)
    cap.set(cv2.CAP_PROP_FPS,30)
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    outmp4 = cv2.VideoWriter(name,fourcc, 30, (640,480))
    while (show):

        # print('======= FOCUSING WHILE ========', focussing)
        # print('======= SHOW ========', show)


        ret, frame = cap.read()
        setFrame(frame)
        if ret:
            if focussing!=True:
                outmp4.write(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
        else:
            break
    # print("======= CAP RELEASE =======")
    cap.release()
    # print("======= CAP RELEASE FINALIZADO=======")
    outmp4.release()
    # print("======= MP4 RELEASE FINALIZADO=======")
    cv2.destroyAllWindows()

def terminar():
    global show, focussing
    show=False
    focussing=True
    return

def evaluate():
    try:
        global posename, show
        finalGrade = evaluateVideo(posename)
        show = True
        return finalGrade
    except print('====== HUBO UN PROBLEMA ======'):
        pass