import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from gesture.gesture import GestureWidget
from menu.appwidget import AppWidget
from cam import Cam

from mind.qt6.emotionQT import EmotionBoard
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
        self.objectDetectionWidget = ObjectWidget(self.cam)
        self.pattenWidget = FindPatterns()
        self.emoWidget = EmotionWidget()
        
        
        level = 1
        self.pattenWidget.make_random_board(level)
        
        # Create a stacked layout and add the widgets
        self.layout = QStackedLayout()
        self.layout.addWidget(self.handTrackWidget)
        #self.layout.addWidget(self.objectDetectionWidget) ; self.objectDetectionWidget.captureThread.start() #    -> Done
        #self.layout.addWidget(self.pattenWidget) #             -> Perfect
        self.layout.addWidget(self.emoWidget) #                -> 

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
    

    def showAppLabel(self, appLabel):
        if self.btn.text() == "<":
            self.btn.setText(">")
            appLabel.show()
        else:
            self.btn.setText("<")
            appLabel.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())