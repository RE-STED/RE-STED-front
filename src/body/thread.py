from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

import time
import cv2
from widget import Pose


class Thread1(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self, cam):
        super().__init__()
        self.running = True
        self.Cam = cam
        self.Pose = Pose()

    def run(self):
        while self.running:
            img = self.Cam.capture()
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

# thread2 for pygame
class Thread2(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        while self.running:
            pass
    
    def on(self):
        self.running = True
    
    def off(self):
        self.running = False