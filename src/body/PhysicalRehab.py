import sys
import cv2

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

sys.path.append('src/body')
from thread import Thread1, Thread2

# ----------------- GUI -----------------

class PoseGUI(QWidget):

    def __init__(self, parent=None, cam=None, data=None):
        super().__init__(parent)
        # self.parent = parent
        self.background = QLabel(self)
        self.background.setContentsMargins(50, 50, 50, 50)
        self.Cam = cam
        self.data = data
        self.background.setStyleSheet("background-color: rgba(0, 0, 0, 30);")
        # print("parent 1", self.parent())
        # print("paren t", self.parent().parent())
        # self.background.resize(self.parent().parent())

        # thread
        self.thread1 = Thread1(parent=self, cam=self.Cam)
        self.thread2 = Thread2(parent=self)

        # params
        self.count = self.thread2.count
        self.working = False # True: working, False: stop

        # button

        # count button
        self.countButton = QPushButton(f'{self.count}')
        self.countButton.setFixedSize(200, 100)
        self.countButton.setStyleSheet("background-color: rgba(0, 200, 0, 200);"
                                            "color: white;"
                                            "font-size: 50px;")
        self.countButton.clicked.connect(self.toggle)

        # title button
        self.titleButton = QPushButton(f'{self.data["joint_name"]} - level: {self.data["level"]}/{self.data["challenge"]}')
        self.titleButton.setStyleSheet("background-color: rgba(255, 255, 255, 200);"
                                            "font-size: 25px;")
        self.titleButton.setFixedHeight(100)

        # home button
        self.homeButton = QPushButton('Home')
        self.homeButton.setFixedSize(200, 100)
        self.homeButton.setStyleSheet("background-color: rgba(0, 0, 0, 200);"
                                            "color: white;"
                                            "font-size: 50px;")
        # self.homeButton.clicked.connect(self.parent.parent.deletePhysicalRehabWidget)



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
        self.buttonWidget = QWidget()
        self.widget = QWidget()
        self.widget.setWindowOpacity(0.0)
        # self.buttonWidget.setWindowOpacity(0.5)
        self.hlayout_button = QHBoxLayout()
        # self.hlayout_button.setContentsMargins(0, 50, 0, 0) # left, top, right, bottom
        self.hlayout_button.addWidget(self.countButton)
        self.hlayout_button.addWidget(self.titleButton)
        self.hlayout_button.addWidget(self.homeButton)
        self.vlayout_button = QVBoxLayout(self.buttonWidget)
        self.vlayout_button.addLayout(self.hlayout_button)
        self.vlayout_button.addWidget(self.widget)

        self.videoWidget = QWidget()
        self.videoWidget.setWindowOpacity(0.5)
        self.hlayout_video = QHBoxLayout(self.videoWidget)
        # self.hlayout_video.setContentsMargins(0, 0, 0, 50)
        self.hlayout_video.addWidget(self.image_pose)
        self.hlayout_video.addWidget(self.image_guide)


        self.slayout = QStackedLayout(self.background)
        self.slayout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.slayout.addWidget(self.buttonWidget)
        self.slayout.addWidget(self.videoWidget)

        # verteical layout
        vlayout = QVBoxLayout()
        vlayout = QVBoxLayout(self.background)
        vlayout.addLayout(self.slayout)
        vlayout.setAlignment(self.slayout, Qt.AlignmentFlag.AlignTop)

        self.background.setLayout(vlayout)

        self.toggle()

    # ----------------- thread 1 -----------------
    def set_thread1(self, image):
        self.image_pose.setPixmap(QPixmap.fromImage(image))

    def start_thread1(self):
        self.thread1 = Thread1(parent=self, cam=self.Cam)
        self.thread1.start()
        self.thread1.updateThread1.connect(self.set_thread1)

    # ----------------- thread 2 -----------------
    def set_thread2(self, image, count):
        self.image_guide.setPixmap(QPixmap.fromImage(image))
        self.count = count
        self.countButton.setText(f'{self.count}')
    
    def start_thread2(self):
        self.thread2 = Thread2(parent=self)
        self.thread2.start()
        self.thread2.updateThread2.connect(self.set_thread2)

        
    def toggle(self):
        if self.working: # stop
            self.working = False
            self.thread1.off()
            self.thread2.off()
            self.countButton.setStyleSheet("background-color: rgba(200, 0, 0, 200);"
                                            "color: white;"
                                            "font-size: 50px;"
                                            )
        else: # start
            self.working = True
            self.start_thread1()
            self.start_thread2()
            self.thread1.on()
            self.thread2.on()
            self.countButton.setStyleSheet("background-color: rgba(0, 200, 0, 200);"
                                            "color: white;"
                                            "font-size: 50px;"
                                            )


# gui2 for pyguide
# gui3 for botton

if __name__ == '__main__':
    data = {"joint_name": "RIGHT_SHOULDER",
                    'level': 3,
                    'challenge': 10}
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
            self.PoseGui = PoseGUI(self, cam=self.Cam, data=data)
            self.setCentralWidget(self.PoseGui.background) # set
            
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()