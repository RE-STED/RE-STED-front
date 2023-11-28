import sys
import os
import time
import cv2

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from thread import Thread1
import numpy as np


# ----------------- GUI -----------------
# gui 1 for pose
class PoseGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.background = QWidget(self)

        # self.cam = cam # cam

        self.startButton = QPushButton('Start Pose Estimation') # botton
        self.startButton.clicked.connect(self.toggle_capture)
        self.is_capturing = False

        self.scene1 = QGraphicsScene(self) # pose
        self.view1 = QGraphicsView(self.scene1)
        self.image_pose = QGraphicsPixmapItem()
        self.scene1.addItem(self.image_pose)

        self.scene2 = QGraphicsScene(self) # game
        self.view2 = QGraphicsView(self.scene2)
        self.image_game = QGraphicsPixmapItem()
        # self.scene2.addItem(self.image_game)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.view1)
        self.hlayout.addWidget(self.view2)

        vlayout = QVBoxLayout()
        vlayout.addLayout(self.hlayout)
        vlayout.addWidget(self.startButton)

        self.background.setLayout(vlayout)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.5)  # 50% opacity
        self.background.setGraphicsEffect(self.opacity_effect)

    def setPose(self, image, height, width):
        self.image_pose.setPixmap(QPixmap.fromImage(image))
        # self.image_height = height
        # self.image_width = width

    # def setGame(self, image, height, width):
    #     self.image_game.setPixmap(QPixmap.fromImage(image))

    def start_pose(self):
        self.thread1 = Thread1()
        self.thread1.updateImg.connect(self.setPose)
        self.thread1.start()

    # def start_game(self):
    #     self.thread1 = Thread1(self.img)
    #     self.thread1.updateImg.connect(self.setPose)
    #     self.thread1.start()
        
    def toggle_capture(self):
        if self.is_capturing: # stop
            self.is_capturing = False
            self.thread1.off()
            self.startButton.setText('Start Pose Estimation')
        else: # start
            self.is_capturing = True
            self.start_pose()
            self.thread1.on()
            self.startButton.setText('Stop Pose Estimation')
    

if __name__ == '__main__':
    class MyApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('RESTED-AI-BODY')
            self.resize(1920, 1080)
            # self.cam = Cam()
            self.PoseGui = PoseGUI()
            self.setCentralWidget(self.PoseGui.background) # set

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()

