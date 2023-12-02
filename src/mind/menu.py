# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import *
import sys

from PyQt6 import uic

MenuWindow = uic.loadUiType("src/mind/qt6/UI/Menu.ui")[0]

class MenuWidget(QWidget, MenuWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # PyQt6
        self.resize(1920, 1080)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 30);")
        
        self.Home.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 48pt; color: white; } QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 50pt;}");
        self.Home.clicked.connect(self.End)

        self.PatternBtn.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 23pt; color: white; } QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 25pt;}");
        self.ODBtn.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 23pt; color: white; } QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 25pt;}");
        self.EmotionBtn.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 23pt; color: white; } QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 25pt;}");
    
    def End(self):
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MenuWidget()
    myWindow.show()
    app.exec()