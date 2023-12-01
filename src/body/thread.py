from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

import cv2
# from body.widget import Pose
from widget import Pose
from avatar import Avatar
import parameter as pm
import function as fn


# ----------------- thread -----------------
# thread1 for pose estimation
class Thread1(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self, cam, parent=None):
        super().__init__()
        self.running = True
        self.Cam = cam
        self.Pose = Pose()
        self.Avatar = Avatar(1920, 1080, parent=self)

    def run(self):
        # cam = Cam()
        while self.running:
            # img load
            img = self.Cam.capture() 
            img = cv2.flip(img, 1)

            # ------ pose estimation ------
            # self.Pose.process(img)
            # img = self.Avatar.process(self.Pose.joint_pos_dict)
            try:
                self.Pose.process(img)
                img = self.Avatar.process(self.Pose.joint_pos_dict)
                img = cv2.flip(img, 1)
                h, w, _ = img.shape
                if w <= 0 or h <= 0:
                    raise Exception
            except:
                print('no pose')
                # init camera pose
                img = self.Cam.capture() 
                h, w, _ = img.shape
                # writing on image in the center red color bigger than cv2.LineAA
                cv2.putText(img, 'Show your face', (int(w/2), int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)

            
            # ------ send img to gui ------
            print(img.shape)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            

            if ch == 1:
                convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_Grayscale8)
            else:
                convertToQtFormat = QImage(img.data, w, h, w * ch, QImage.Format.Format_RGB888)
            scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(), Qt.TransformationMode.FastTransformation)
            self.updateImg.emit(scaledImage, scaledImage.width(), scaledImage.height())
        
            pm.firstRun = 1

    def on(self):
        self.running = True

    def off(self):
        self.running = False

# thread2 for guide
class Thread2(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.cam = cv2.VideoCapture('data/video/LEFT_ELBOW.mp4')
    
    def run(self):
        while self.running:
            pass
    
    def on(self):
        self.running = True
    
    def off(self):
        self.running = False