import sys
import os
import time

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import cv2
import mediapipe as mp
import numpy as np


# main window
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RESTED-AI-BODY')
        self.resize(1920, 1080)

        self.PoseGui = PoseGUI()
        self.setCentralWidget(self.PoseGui.background) # set


# ----------------- thread -----------------
# thread1 for pose estimation
class Thread1(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self):
        super().__init__()
        self.running = True
        self.Cam = Cam()
        self.Pose = Pose()

    def run(self):
        # cam = Cam()
        while self.running:
            img = self.Cam.capture()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = True
            img, landmarks = self.Pose.pose_detect(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            
            convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(), Qt.TransformationMode.FastTransformation)
            self.updateImg.emit(scaledImage, scaledImage.width(), scaledImage.height())
            

    def on(self):
        self.running = True

    def off(self):
        self.running = False

class Pose(QWidget):
    def __init__(self):
        super().__init__()
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()

    def pose_detect(self, img):
        results = self.pose.process(img)
        landmarks = results.pose_landmarks
        print(landmarks)
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

# thread2 for cam
class Cam():
    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        
    def capture(self):
        ret, frame = self.cam.read()
        if ret:
            # color change
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # flip
            img = cv2.flip(img, 1)
            return img         
            
# thread3 for botton


# thread4 for pygame
# ----------------- GUI -----------------
# gui1 for pose

class PoseGUI(QWidget):
    def __init__(self):
        super().__init__()
        # cam
        self.background = QLabel(self)

        # thread
        self.thread1 = Thread1()

        # button
        self.startButton = QPushButton('Start Pose Estimation')
        self.startButton.clicked.connect(self.toggle_capture)
        self.is_capturing = False

        # pose screen
        self.scene1 = QGraphicsScene(self)
        self.view1 = QGraphicsView(self.scene1)
        self.image_pose = QGraphicsPixmapItem()
        self.scene1.addItem(self.image_pose)

        # game screen
        self.scene2 = QGraphicsScene(self)
        self.view2 = QGraphicsView(self.scene2)
        self.image_game = QGraphicsPixmapItem()
        # self.scene2.addItem(self.image_game)

        # horizion layout
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.view1)
        self.hlayout.addWidget(self.view2)

        # verteical layout
        vlayout = QVBoxLayout(self.background)
        vlayout.addLayout(self.hlayout)
        vlayout.addWidget(self.startButton)

        self.background.setLayout(vlayout)

          # 원하는 업데이트 간격을 밀리초 단위로 설정
    def setPose(self, image, height, width):
        self.image_pose.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width

    def start_thread1(self):
        self.thread1.start()
        self.thread1.updateImg.connect(self.setPose)
        
    def toggle_capture(self):
        if self.is_capturing: # stop
            self.is_capturing = False
            self.thread1.off()
            self.startButton.setText('Start Pose Estimation')
        else: # start
            self.is_capturing = True
            self.start_thread1()
            self.thread1.on()
            self.startButton.setText('Stop Pose Estimation')


# gui2 for pygame
# gui3 for botton

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()