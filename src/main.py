import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from gesture.gesture import GestureWidget
from menu.appwidget import AppWidget
from cam import Cam

from mind.menu import MenuWidget
from mind.quiz.emotion import EmotionWidget
from mind.quiz.pattern import FindPatterns
from mind.quiz.object import ObjectWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cam = Cam()
        self.setWindowTitle('Hand Tracking with PyQt')
        self.getFullScreen()
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        self.handTrackWidget = GestureWidget(self, self.cam)
        self.mindMeneWidget = MenuWidget()
        
        self.mindMeneWidget.PatternBtn.clicked.connect(self.pattern)
        self.mindMeneWidget.EmotionBtn.clicked.connect(self.emotion)
        self.mindMeneWidget.ODBtn.clicked.connect(self.object)
        
        # Create a stacked layout and add the widgets
        self.layout = QStackedLayout()
        self.layout.addWidget(self.handTrackWidget)

        self.layout.addWidget(self.mindMeneWidget)
        
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        #self.layout.setCurrentWidget(self.appLabel)
        # self.addAppLabelWidget()
        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        

    def getFullScreen(self):
        self.showFullScreen()


    def addAppLabelWidget(self):
        self.appLabelWidget = AppWidget(self)
        self.layout.addWidget(self.appLabelWidget.appLabelWidget)
        self.layout.setCurrentWidget(self.appLabelWidget.appLabelWidget)
        #self.appLabelWidget.appLabelWidget.hide()
    

    def pattern(self):
        self.setPatternWidget()
        self.patternWidget.make_random_board(2)
        self.layout.addWidget(self.patternWidget)
        self.mindMeneWidget.hide()
        self.layout.setCurrentWidget(self.patternWidget)
    
    def emotion(self):
        self.setEmotionWidget()
        self.layout.addWidget(self.emotionWidget)
        self.mindMeneWidget.hide()
        self.layout.setCurrentWidget(self.emotionWidget)
    
    def object(self):
        self.setObjectWidget()
        self.layout.addWidget(self.objectWidget)
        self.mindMeneWidget.hide()
        self.layout.setCurrentWidget(self.objectWidget)
        self.objectWidget.captureThread.start()
        
    def setPatternWidget(self):
        self.patternWidget = FindPatterns()
        self.patternWidget.parent = self
        self.patternWidget.HomeButton.clicked.connect(self.gameHomeBtn)
        
    def setEmotionWidget(self):
        self.emotionWidget = EmotionWidget()
        self.emotionWidget.parent = self
        self.emotionWidget.HomeButton.clicked.connect(self.gameHomeBtn)
    
    def setObjectWidget(self):
        self.objectWidget = ObjectWidget(cam=self.cam)
        self.objectWidget.parent = self
        self.objectWidget.HomeButton.clicked.connect(self.gameHomeBtn)
        
    def gameHomeBtn(self):
        #지금 QStackedLayout 가장 위에 있는 위젯을 제거하고 MenuWidget을 보여줌
        self.layout.removeWidget(self.layout.currentWidget())
        self.mindMeneWidget.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())