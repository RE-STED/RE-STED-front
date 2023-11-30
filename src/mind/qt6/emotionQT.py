import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
import time
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation

class EmotionBoard(QStackedWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/mind/qt6/UI/EmotionBoard.ui", self)
        
        self.widget(0).findChild(QLabel, "label").setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 120); font-size: 48pt; color: white; }")
        self.widget(1).findChild(QLabel, "Title").setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 120); font-size: 48pt; color: white; }")
        self.widget(1).findChild(QLabel, "name").setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 120); font-size: 48pt; color: white; }")
        self.widget(1).findChild(QLabel, "ImgForGroup").hide()
        self.widget(1).findChild(QLabel, "ImgForOne").hide()
        
        self.widget(2).findChild(QPushButton, "SadBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "AngryBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "HappyBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "FearfulBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "SurpriseBtn_2").setFlat(False)
        self.widget(2).findChild(QPushButton, "NeutralBth_2").setFlat(False)
        
        
        self.setBtnStyle(self.widget(0).findChild(QPushButton, "SelectCeleb"))

        self.setBtnStyle(self.widget(0).findChild(QPushButton, "SelectFamily"))
        
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "SadBtn_2"))
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "AngryBtn_2"))
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "HappyBtn_2"))
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "NeutralBth_2")) 
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "FearfulBtn_2")) 
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "SurpriseBtn_2")) 
        
        self.setBtnStyle(self.widget(2).findChild(QPushButton, "InputAnswer"))
        
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "SadBtn")) 
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "AngryBtn")) 
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "HappyBtn")) 
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "NeutralBth")) 
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "FearfulBtn")) 
        self.setBtnStyle(self.widget(3).findChild(QPushButton, "SurpriseBtn")) 
    
    
    
    def setBtnStyle(self, btn):
        #btn.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 100); font-size: 30pt; color: white; border-radius: 1.5em;} QPushButton:hover { background-color: rgba(255, 255, 255, 150); font-weight: bold; font-size: 35pt;}");
        btn.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 120); font-size: 30pt; color: white; border-radius: 1.5em;} QPushButton:hover { background-color: rgba(200, 200, 200, 150); font-weight: bold; font-size: 35pt;}");

        

        

# class EmotionWindow(QMainWindow):
#     stack = EmotionBoard()
#     def __init__(self):
#         super().__init__()
        
#         self.setCentralWidget(self.stack)
        
#         self. widget(0).findChild(QPushButton, "pushButton_2") 
#         self. widget(1).findChild(QPushButton, "pushButton").clicked.connect(self.end)
        
#     def start(self):
#         self. setCurrentIndex(1)
        
#     def end(self):
#         self. setCurrentIndex(0)