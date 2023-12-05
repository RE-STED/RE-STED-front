import sys
import cv2

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

sys.path.append('src/body')
from thread import Thread1, Thread2

# ----------------- GUI -----------------

class PhysicalRehabWidget(QWidget):

    def __init__(self, parent=None, cam=None):
        super().__init__()
        # cam
        self.background = QLabel(self)
        self.Cam = cam
        # self.joint_name = self.parent.joint_name
        self.joint_name = "RIGHT_SHOULDER"

        # thread
        self.thread1 = Thread1(parent=self, cam=self.Cam)
        self.thread2 = Thread2(parent=self)

        # button
        self.startButton = QPushButton('Start Pose Estimation')
        self.startButton.clicked.connect(self.toggle_capture)
        self.is_capturing = False

        # pose screen
        self.scene1 = QGraphicsScene(self)
        self.view1 = QGraphicsView(self.scene1)
        self.view1.scale(0.4, 0.4)
        self.image_pose = QGraphicsPixmapItem()
        self.scene1.addItem(self.image_pose)

        # guide screen
        self.scene2 = QGraphicsScene(self)
        self.view2 = QGraphicsView(self.scene2)
        self.view2.scale(0.4, 0.4)
        self.image_guide = QGraphicsPixmapItem()
        self.scene2.addItem(self.image_guide)

        # horizion layout
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.view1)
        self.hlayout.addWidget(self.view2)

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
            self.PoseGui = PhysicalRehabWidget(self, self.Cam)
            self.setCentralWidget(self.PoseGui.background) # set
            
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()