# hand tracking 하는 모델을 만들어서 사용할 수 있도록 하는 모듈

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import os, sys
import cv2
import time
from PyQt6.QtGui import QCursor, QGuiApplication

cam = cv2.VideoCapture(0)

cwd = os.getcwd()
print(cwd)
model_path = os.path.join(cwd, 'RND', 'hand_landmarker.task')
print(model_path)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

app = QGuiApplication(sys.argv)
screenGeometry = QGuiApplication.primaryScreen().geometry()

# Create a hand landmarker instance with the live stream mode:
def moveCursor(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    #print(result)
    # Move mouse cursor to the center of the hand using PyQt5’s QCursor#setPos method.
    if result.hand_landmarks:
        # print(result.hand_landmarks[0][0].x, result.hand_landmarks[0][0].y)
        # print(result.hand_landmarks[0][0].x * output_image.width, result.hand_landmarks[0][0].y * output_image.height)
        print(screenGeometry.x(), screenGeometry.y())
        QCursor.setPos(screenGeometry.x() + result.hand_landmarks[0][0].x * output_image.width, 
                    screenGeometry.y() + result.hand_landmarks[0][0].y * output_image.height)
        QGuiApplication.processEvents()  # Process Qt events


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=moveCursor)

with HandLandmarker.create_from_options(options) as landmarker:
    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    # Create a loop to read the latest frame from the camera using VideoCapture#read()
    # Convert the frame received from OpenCV to a MediaPipe’s Image object.

    while True:
        # Prepare Data
        if cv2.waitKey(1) == ord('q'):
            break
        success, img = cam.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        frame_timestamp_ms = int(1000 * time.time())
        # Call the process method passing the image.
        # The process method will return the annotated image and the hand landmarks.
        # Convert the annotated image back to OpenCV’s BGR format.
        # Display the image in a window using OpenCV’s imshow function.
        # Press ‘q’ to exit the loop.

        # Run the Task
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        # Show image on OpenCV Window
        cv2.imshow("Image", img)

        # Draw landmarks on the image


cv2.destroyAllWindows()

