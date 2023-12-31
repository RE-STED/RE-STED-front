import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
import time
from PyQt6.QtCore import QTimer

Board, T = uic.loadUiType("src/mind/qt6/UI/DetectionPage.ui")
class DetectionWidget(QWidget, Board):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 포함하는 위젯 목록 출력
            
        
    def show_ending_message(self, Result: bool):
        
        '''
        True 면 정답 메시지를 띄우고 창 닫기
        False 면 오답 메시지를 띄우고 확인을 누르면 진행하던 게임을 계속 진행
        '''
        if Result:
            QMessageBox.about(self, "정답", "정답입니다!")
            time.sleep(1)
            self.close()
        else:
            QMessageBox.about(self, "오답", "[빠진 문자]가 있는지 \n또는\n [숨겨진 숫자]를 확인해주세요!")
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    StartWindow = DetectionWidget()
    StartWindow.show()

    app.exec()


