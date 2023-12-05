import typing
import sys
import json
import time
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QMouseEvent
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QCoreApplication, QEvent

sys.path.append('src')

from mind.utils.util import select_level
from mind.quiz.pattern import FindPatterns
from mind.quiz.emotion import EmotionWidget
from mind.quiz.object import ObjectWidget

class AppButton(QPushButton):
    buttonClicked = pyqtSignal(int)  # 사용자 정의 신호 생성

    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.setStyleSheet(
            'background: black; color: white; font-size: 25px; border-radius: 1.5em;'
        )
        # Create a QGraphicsOpacityEffect object
        self.opacity_effect = QGraphicsOpacityEffect(self)
        # Set the opacity level. The value should be between 0 (completely transparent) and 1 (completely opaque).
        self.opacity_effect.setOpacity(0.2)
        # Apply the opacity effect to the button
        self.setGraphicsEffect(self.opacity_effect)

    # def enterEvent(self, event):
    #     self.opacity_effect.setOpacity(0.6)
    #     self.setGraphicsEffect(self.opacity_effect)

    # def leaveEvent(self, event):
    #     self.opacity_effect.setOpacity(0.2)
    #     self.setGraphicsEffect(self.opacity_effect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.opacity_effect.setOpacity(0.7)
            self.setGraphicsEffect(self.opacity_effect)
        return super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.opacity_effect.setOpacity(0.2)
            self.setGraphicsEffect(self.opacity_effect)
            self.buttonClicked.emit(self.index)  # buttonClicked 신호 발생

        return super().mouseReleaseEvent(event)



class AppButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        self.buttons = []

        for i in range(3):
            if(i == 0):
                button = AppButton(i, f'Mind Quiz', self)
            elif(i == 1):
                button = AppButton(i, f'Find Something', self)
            elif(i == 2):
                button = AppButton(i, f'Guess Face', self)
            
            button.setFixedSize(170, 170)

            self.buttons.append(button)
            self.vlayout.addWidget(button)
            #print(button.size().width(), button.size().height())
        print(button)
        self.vlayout.addStretch()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())


    def connectButtonClicked(self, handler):
        for button in self.buttons:
            button.buttonClicked.connect(handler)



class CognitiveRehabWidget(QWidget):
    def __init__(self, cam, parent=None):
        super().__init__(parent)
        
        self.cam = cam 
        
        appLabelLayout = QHBoxLayout()
        appLabelLayout.setContentsMargins(50, 50, 50, 50)  # Set all margins to 50
        appLabelLayout.addStretch()

        self.layout = QStackedLayout()

        menuLayout = QVBoxLayout()
        menuLayout.addStretch()
        resultButton = QPushButton("Result", self)
        resultButton.setFixedSize(130, 130)
        resultButton.setStyleSheet(
            'background: rgba(0, 0, 0, 0.5); color: white; font-size: 25px; border-radius: 1em;'
            'hover { background: rgba(0, 0, 0, 0.8); }'
        )
        menuLayout.addWidget(resultButton)
        #resultButton.clicked.connect()

        homeButton = QPushButton("Home", self)
        homeButton.setFixedSize(130, 130)
        homeButton.setStyleSheet(
            'background: rgba(0, 0, 0, 0.5); color: white; font-size: 25px; border-radius: 1em;'
            'hover { background: rgba(0, 0, 0, 0.8); }'
        )
        menuLayout.addWidget(homeButton)
        menuLayout.addStretch()
        homeButton.clicked.connect(self.parent().deleteCognitiveRehabWidget)
        
        appLabelLayout.addLayout(menuLayout)

        self.appLabel = AppButtonsWidget(self)
        self.appLabel.connectButtonClicked(self.handleButtonClicked)
        appLabelLayout.addWidget(self.appLabel)
        
        self.btnWidget = QWidget(self)
        self.btnWidget.setLayout(appLabelLayout)

        # self.appLabelWidget = QWidget(self)
        
        self.layout.addWidget(self.btnWidget)
        
        self.setLayout(self.layout)
        
        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.setStyleSheet("background-color: transparent;")
        
        # Result
        
        # mind/Result.json를 불러와서 self.RecoredResultDict에 딕셔너리 형태로 저장
        with open('src/mind/Result.json', 'r', encoding='utf-8') as f:
            self.RecordResultDict = json.load(f)
        
        # today에 오늘 날짜를 YY-MM-DD 형태로 저장
        self.today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if self.today not in self.RecordResultDict.keys():
            self.RecordResultDict[self.today] = {}
            self.RecordResultDict[self.today]['Pattern'] = []
            self.RecordResultDict[self.today]['Object'] = []
            self.RecordResultDict[self.today]['Emotion'] = []


    def handleButtonClicked(self, index):
        if(index == 0):
            print("Pattern Quiz")
            self.pattern()
        elif(index == 1):
            print("Find Something")
            self.object()
        elif(index == 2):
            print("Guess Face")
            self.emotion()
            
    def pattern(self):
        self.setPatternWidget()
        self.patternWidget.make_random_board(select_level(self.RecordResultDict))
        self.layout.addWidget(self.patternWidget)
        self.btnWidget.hide()
        self.layout.setCurrentWidget(self.patternWidget)
    
    def emotion(self):
        print("emotion")
        self.setEmotionWidget()
        self.layout.addWidget(self.emotionWidget)
        self.btnWidget.hide()
        self.layout.setCurrentWidget(self.emotionWidget)
    
    def object(self):
        self.setObjectWidget()
        self.layout.addWidget(self.objectWidget)
        self.btnWidget.hide()
        self.layout.setCurrentWidget(self.objectWidget)
        self.objectWidget.captureThread.start()
        
    def setPatternWidget(self):
        patternResult = {"Time":None, 'Pattern' : None, 'Number' : None, 'Score': -1}
        self.patternWidget = FindPatterns(patternResult)
        self.patternWidget.parent = self
        self.patternWidget.HomeButton.clicked.connect(self.gameHomeBtn)
        
    def setEmotionWidget(self):
        emotionResult = {'Time':None, 'Emotion' : None, 'Score': 100, 'Who': ''}
        
        self.emotionWidget = EmotionWidget(emotionResult)
        self.emotionWidget.parent = self
        self.emotionWidget.HomeButton.clicked.connect(self.gameHomeBtn)
    
    def setObjectWidget(self):
        objectResult = {'Time':None, 'Object' : None, 'Success': None}
        
        self.objectWidget = ObjectWidget(cam=self.cam, Result=objectResult)
        self.objectWidget.parent = self
        self.objectWidget.HomeButton.clicked.connect(self.gameHomeBtn)

    def gameHomeBtn(self):
        #지금 QStackedLayout 가장 위에 있는 위젯을 제거하고 MenuWidget을 보여줌
        print("삭제 전", self.layout.currentWidget())
        self.layout.removeWidget(self.layout.currentWidget())
        print("삭제 후", self.layout.currentWidget())
        self.btnWidget.show()
        