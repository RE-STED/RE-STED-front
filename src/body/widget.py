from PyQt6.QtWidgets import QWidget
import cv2
import mediapipe as mp

class Pose(QWidget):
    def __init__(self):
        super().__init__()
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()

    def pose_detect(self, img):
        results = self.pose.process(img)
        landmarks = results.pose_landmarks.landmark
        self.draw_landmarks(img, results)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img, landmarks

    def draw_landmarks(self, img, results):
        self.mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )