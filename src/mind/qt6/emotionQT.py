import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
import time
from PyQt6.QtCore import QTimer

class EmotionBoard(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/mind/qt6/UI/EmotionBoard.ui", self)
        
        self.widget(2).findChild(QPushButton, "SadBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "AngryBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "HappyBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "FearfulBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "SurpriseBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "NeutralBth_2").setFlat(False)

        

# class EmotionWindow(QMainWindow):
#     stack = EmotionBoard()
#     def __init__(self):
#         super().__init__()
        
#         self.setCentralWidget(self.stack)
        
#         self.stack.widget(0).findChild(QPushButton, "pushButton_2").clicked.connect(self.start)
#         self.stack.widget(1).findChild(QPushButton, "pushButton").clicked.connect(self.end)
        
#     def start(self):
#         self.stack.setCurrentIndex(1)
        
#     def end(self):
#         self.stack.setCurrentIndex(0)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    StartWindow = EmotionWindow()
    StartWindow.show()

    app.exec()