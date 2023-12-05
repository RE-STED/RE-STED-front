import sys
import cv2

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

sys.path.append('src/body')
from thread import Thread1, Thread2

# ----------------- GUI -----------------

class PoseGUI(QWidget):

    def __init__(self, parent=None, cam=None, joint_name=None):
        super().__init__()
        self.background = QLabel(self)
        self.Cam = cam
        self.joint_name = joint_name
        self.background.setStyleSheet("background-color: rgba(0, 0, 0, 30);")

        # thread
        self.thread1 = Thread1(parent=self, cam=self.Cam)
        self.thread2 = Thread2(parent=self)

        # button
        self.startButton = QPushButton('Start Pose Estimation')
        self.startButton.clicked.connect(self.toggle_capture)
        self.is_capturing = False

        opacity_effect_pose = QGraphicsOpacityEffect()
        opacity_effect_pose.setOpacity(0.5)  # 0.0부터 1.0까지의 값을 설정하여 투명도를 조절할 수 있습니다.
        opacity_effect_guide = QGraphicsOpacityEffect()
        opacity_effect_guide.setOpacity(0.5)  # 0.0부터 1.0까지의 값을 설정하여 투명도를 조절할 수 있습니다.
        

        self.image_pose = QLabel()
        self.image_pose.setScaledContents(True)
        self.image_pose.setGraphicsEffect(opacity_effect_pose)

        self.image_guide = QLabel()
        self.image_guide.setScaledContents(True)
        self.image_guide.setGraphicsEffect(opacity_effect_guide)

        # horizion layout
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.image_pose)
        self.hlayout.addWidget(self.image_guide)

        vlayout = QVBoxLayout()
        # verteical layout
        vlayout = QVBoxLayout(self.background)
        vlayout.addLayout(self.hlayout)
        vlayout.addWidget(self.startButton)

        self.background.setLayout(vlayout)

    # ----------------- thread 1 -----------------
    def set_thread1(self, image, height, width):
        self.image_pose.setPixmap(QPixmap.fromImage(image))

    def start_thread1(self):
        self.thread1 = Thread1(parent=self, cam=self.Cam)
        self.thread1.start()
        self.thread1.updateImg.connect(self.set_thread1)

    # ----------------- thread 2 -----------------
    def set_thread2(self, image, height, width):
        self.image_guide.setPixmap(QPixmap.fromImage(image))
    
    def start_thread2(self):
        self.thread2 = Thread2(parent=self)
        self.thread2.start()
        self.thread2.updateImg.connect(self.set_thread2)

        
    def toggle_capture(self):
        if self.is_capturing: # stop
            self.is_capturing = False
            self.thread1.off()
            self.thread2.off()
            self.startButton.setText('Start Pose Estimation')
        else: # start
            self.is_capturing = True
            self.start_thread1()
            self.start_thread2()
            self.thread1.on()
            self.thread2.on()
            self.startButton.setText('Stop Pose Estimation')


# gui2 for pyguide
# gui3 for botton

if __name__ == '__main__':
    class Cami():
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
    # main window
    class MyApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('RESTED-AI-BODY')
            self.resize(1920, 1080)
            self.Cam = Cami()
            self.PoseGui = PoseGUI(self, self.Cam, joint_name='RIGHT_SHOULDER')
            self.setCentralWidget(self.PoseGui.background) # set
            
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()