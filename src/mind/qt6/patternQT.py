import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
import time
from PyQt6.QtCore import QTimer

Board = uic.loadUiType("src/mind/qt6/UI/PatternBoard.ui")[0]

class PatternWindow(QWidget, Board):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def set_btn(self):
        for i in range(9):
            for j in range(9):
                #eval(f'self.p{i}{j}.setFlat(True)')
                #self.GameBoard = self.findChild(QGridLayout, "GameBoard")
                self.GameBoard.itemAtPosition(i, j).widget().setFlat(True)
                self.GameBoard.itemAtPosition(i, j).widget().clicked.connect(self.fnc_flat)
    
        
    def fnc_flat(self):
        btn = self.sender()
        btn.setFlat(not btn.isFlat())
        
    def show_ending_message(self, Result: bool):
        
        '''
        True 면 정답 메시지를 띄우고 창 닫기
        False 면 오답 메시지를 띄우고 확인을 누르면 진행하던 게임을 계속 진행
        '''
        if Result:
            QMessageBox.about(self, "정답", "정답입니다!")
            time.sleep(1)
            self.close_window()
        else:
            QMessageBox.about(self, "오답", "[빠진 문자]가 있는지 \n또는\n [숨겨진 숫자]를 확인해주세요!")
            
    def set_style(self, btn):
        btn.setStyleSheet("QPushButton { background-color: white; font-size: 30pt; color: black; } QPushButton:hover { font-weight: bold; font-size: 33pt;}");
        
    def close_window(self):
        for i in range(100):
            i = i / 100
            self.setWindowOpacity(1 - i)
            time.sleep(0.005)
        self.close()
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    StartWindow = PatternWindow()
    StartWindow.show()

    app.exec()