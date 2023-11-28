import sys
import os
import time

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import cv2
import mediapipe as mp
import numpy as np

# from widget import Pose
from thread import Thread1

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
# ----------------- GUI -----------------

class PoseGUI(QWidget):
    def __init__(self, parents=None, cam=None):
        super().__init__()
        # cam
        self.background = QLabel(self)
        self.Cam = cam

        # thread
        self.thread1 = Thread1(self.Cam)
        # self.thread1 = Thread2()

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
    def set_thread1(self, image, height, width):
        self.image_pose.setPixmap(QPixmap.fromImage(image))

    def start_thread1(self):
        self.thread1 = Thread1(self.Cam)
        self.thread1.start()
        self.thread1.updateImg.connect(self.set_thread1)

    # def set_thread2(self, image, height, width):
    #     self.image_game.setPixmap(QPixmap.fromImage(image))
    
    # def start_thread2(self):
    #     self.thread2.start()
    #     self.thread2.updateImg.connect(self.set_thread2)
        
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
    # main window
    class MyApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('RESTED-AI-BODY')
            self.resize(1920, 1080)
            self.Cam = Cam()
            self.PoseGui = PoseGUI(self, self.Cam)
            self.setCentralWidget(self.PoseGui.background) # set
            
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()