import typing, sys
sys.path.append('src')
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QMouseEvent
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QCoreApplication, QEvent

from body.PhysicalRehab import PoseGUI
from functools import partial

class AppButton(QPushButton):
    buttonClicked = pyqtSignal(int)  # 사용자 정의 신호 생성

    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.parent = parent
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



class LevelButton(QPushButton):
    buttonClicked = pyqtSignal(int)  # 사용자 정의 신호 생성

    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.parent = parent
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

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
    
    def setButtonChecked(self):
        self.opacity_effect.setOpacity(0.7)
        self.setStyleSheet('background: white; color: black; font-size: 25px; border-radius: 1.5em;')
        self.setGraphicsEffect(self.opacity_effect)

    def setButtonUnchecked(self):
        self.opacity_effect.setOpacity(0.2)
        self.setStyleSheet('background: black; color: white; font-size: 25px; border-radius: 1.5em;')
        self.setGraphicsEffect(self.opacity_effect) 


class AppButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        self.buttons = []

        for i in range(4):
            if(i == 0):
                button = AppButton(i, f'오른쪽\n어깨', self)
            elif(i == 1):
                button = AppButton(i, f'오른쪽\n팔꿈치', self)
            elif(i == 2):
                button = AppButton(i, f'오른쪽\n무릎', self)
            elif(i == 3):
                button = AppButton(i, f'+', self)
            
            button.setFixedSize(170, 170)

            self.buttons.append(button)
            self.vlayout.addWidget(button)
            #print(button.size().width(), button.size().height())

        self.vlayout.addStretch()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())

    def connectButtonClicked(self, handler):
        for button in self.buttons:
            button.buttonClicked.connect(handler)



class LevelButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        self.buttons = []

        for i in range(9):
            button = LevelButton(i, f'{i+1}', self)
            button.clicked.connect(partial(parent.levelButtonClicked, i))  # Bind level value to handler
            button.setFixedSize(70, 70)

            self.buttons.append(button)
            self.vlayout.addWidget(button)

        self.vlayout.addStretch()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())


class PhysicalRehabWidget(QWidget):    
    def __init__(self, parent, cam):
        super().__init__(parent)
        
        self.cam = cam
        self.level = 1
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
        homeButton.clicked.connect(self.parent().deletePhysicalRehabWidget)
        
        appLabelLayout.addLayout(menuLayout)

        levelLayout = QVBoxLayout()
        self.levelWidget = LevelButtonsWidget(self)
        levelLayout.addWidget(self.levelWidget)
        appLabelLayout.addLayout(levelLayout)

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


    def levelButtonClicked(self, button_index):
        self.level = button_index + 1
        print(f"Level {self.level} clicked")

        for button in self.levelWidget.buttons:
            button.setButtonUnchecked()
        
        self.levelWidget.buttons[button_index].setButtonChecked()

    
    # AppButton이 클릭될 때 실행되는 슬롯
    def handleButtonClicked(self, button_index):
        if button_index == 0:
            print("0번째 운동 실행")
            data = {"joint_name": "RIGHT_SHOULDER",
                    'level': self.level,
                    'challenge': 10}
            
        elif button_index == 1:
            print("1번째 운동 실행")
            data = {"joint_name": "RIGHT_ELBOW",
                    'level': self.level,
                    'challenge': 10}
            
        elif button_index == 2:
            print("2번째 운동 실행")
            data = {"joint_name": "RIGHT_KNEE",
                    'level': self.level,
                    'challenge': 10}
            
        elif button_index == 3:
            print("운동 추가")
            data = {"joint_name": "RIGHT_SHOULDER",
                    'level': self.level,
                    'challenge': 10}
        self.excercise(data)
            
    def excercise(self, data):
        self.poseWidget = PoseGUI(self, self.cam, data)
        self.layout.addWidget(self.poseWidget.background)
        self.btnWidget.hide()
        self.layout.setCurrentWidget(self.poseWidget.background)
