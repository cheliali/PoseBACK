from asyncio.windows_events import NULL
import cv2

cap = NULL
face_detector = NULL

def iniciar():
    print("innicia")
    global cap 
    global face_detector
    cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 
        "haarcascade_frontalface_default.xml")

def generate():
    global cap 
    global face_detector
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
    
def terminar():
    global cap
    print("terminar")
    cap.release()