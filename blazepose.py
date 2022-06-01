import cv2
import mediapipe as mp
import random

cap = None

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    
def generate():
    try:
        global cap
        mp_drawing=mp.solutions.drawing_utils
        mp_pose=mp.solutions.pose

        with mp_pose.Pose(
            static_image_mode=False) as pose:

            while True:
                hasFrame, frame= cap.read()
                if hasFrame:
                    
                    # n = random.randint(0,15)
                    # prev = 0
                    # if(n > prev):
                    #     print(n)
                    #     cv2.imwrite(str(n)+"frame.jpg", frame) 

                    frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results=pose.process(frame_rgb)

                    if results.pose_landmarks is not None:
                        mp_drawing.draw_landmarks(
                            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                            mp_drawing.DrawingSpec(color=(128,0,250), thickness=2, circle_radius=3),
                            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
                            )
                else:
                    cap.release()

                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
    except Exception as e:
        pass

def terminar():
    global cap
    cap.release()
    return

