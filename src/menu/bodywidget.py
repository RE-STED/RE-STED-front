from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QMouseEvent
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QCoreApplication, QEvent

class AppButton(QPushButton):
    buttonClicked = pyqtSignal(int)  # 사용자 정의 신호 생성

    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.setStyleSheet(
            'background: black; color: white; font-size: 20px; border-radius: 1.5em;'
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



class PhysicalRehabWidget(QWidget):
    def __init__(self, parent: None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        self.buttons = []

        for i in range(3):
            if(i == 0):
                button = AppButton(i, f'Shoulder', self)
            elif(i == 1):
                button = AppButton(i, f'Elbow', self)
            elif(i == 2):
                button = AppButton(i, f'Wrist', self)
            
            button.setFixedSize(200, 200)

            self.buttons.append(button)
            self.vlayout.addWidget(button)
            #print(button.size().width(), button.size().height())

        self.vlayout.addStretch()
        # create a horizontal layout and add stretch so everything is 
        # pushed to the right

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())

    def connectButtonClicked(self, handler):
        for button in self.buttons:
            button.buttonClicked.connect(handler)
