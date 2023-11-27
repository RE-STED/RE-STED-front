import sys
import os
import time
import cv2

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from thread import Thread1


# ----------------- GUI -----------------
# gui 1 for pose
class PoseGUI(QWidget):
    def __init__(self, parent=None, cam=None):
        super().__init__(parent)

        # botton
        self.startButton = QPushButton('Start Pose Estimation')
        self.startButton.clicked.connect(self.toggle_capture)
        self.is_capturing = False
        
        # cam
        self.cam = cam
        self.background = QWidget(self)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        layout = QVBoxLayout(self.background)
        layout.addWidget(self.view)
        layout.addWidget(self.startButton)

        self.background.setLayout(layout)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.5)  # 50% opacity
        self.background.setGraphicsEffect(self.opacity_effect)

    def setImage(self, image, height, width):
        self.image_item.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width

    def start_video(self):
        self.thread1 = Thread1(self.cam)
        self.thread1.updateImg.connect(self.setImage)
        self.thread1.start()
        
    def toggle_capture(self):
        if self.is_capturing: # stop
            self.is_capturing = False
            self.thread1.off()
            self.startButton.setText('Start Pose Estimation')
        else: # start
            self.is_capturing = True
            self.start_video()
            self.thread1.on()
            self.startButton.setText('Stop Pose Estimation')


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
        
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RESTED-AI-BODY')
        self.resize(1920, 1080)
        self.cam = Cam()
        self.PoseGui = PoseGUI(self, self.cam)
        self.setCentralWidget(self.PoseGui.background) # set

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()

