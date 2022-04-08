import cv2
import mediapipe as mp

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)

def generate():
    global cap
    mp_drawing=mp.solutions.drawing_utils
    mp_pose=mp.solutions.pose

    cap=cv2.VideoCapture(1)

    with mp_pose.Pose(
        static_image_mode=False) as pose:

        while True:
            hasFrame, frame= cap.read()
            if hasFrame:

                frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results=pose.process(frame_rgb)

                if results.pose_landmarks is not None:
                    mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                        mp_drawing.DrawingSpec(color=(128,0,250), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
                        )

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

def terminar():
    global cap 
    cap.release()

