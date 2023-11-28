from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QMouseEvent
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QCoreApplication, QEvent



class HoverButton(QPushButton):
    # Define a signal for click events
    
    def __init__(self, text, parent=None, size=QSize(190, 190)):
        super().__init__(text, parent)
        self.defaultSize = size
        self.hoverSize = QSize(size.width() + 6, size.height())
        self.setStyleSheet(
            "background-color: black; color: white; font-size: 20px; border-radius: 1.5em;"
        )
        self.setMinimumSize(self.defaultSize)
        # Create a QGraphicsOpacityEffect object
        self.opacity_effect = QGraphicsOpacityEffect(self)
        # Set the opacity level. The value should be between 0 (completely transparent) and 1 (completely opaque).
        self.opacity_effect.setOpacity(0.4)
        # Apply the opacity effect to the button
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self, b"size", self)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

    def enterEvent(self, event):
        # self.opacity_effect.setOpacity(0.6)
        # self.setGraphicsEffect(self.opacity_effect)
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.hoverSize)
        self.animation.start()

    def leaveEvent(self, event):
        # self.opacity_effect.setOpacity(0.2)
        # self.setGraphicsEffect(self.opacity_effect)
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.defaultSize)
        self.animation.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.opacity_effect.setOpacity(0.7)
            self.setGraphicsEffect(self.opacity_effect)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.opacity_effect.setOpacity(0.2)
            self.setGraphicsEffect(self.opacity_effect)
        return super().mouseReleaseEvent(event)


class AppButton(QPushButton):
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
        return super().mouseReleaseEvent(event)


class ClickableLabel(QLabel):
    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.4)  # 50% opacity
        self.setGraphicsEffect(self.opacity_effect)

        # Define a signal for click events
        self.clicked = pyqtSignal(int)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.opacity_effect.setOpacity(0.7)
            self.setGraphicsEffect(self.opacity_effect)

        return super().mousePressEvent(event)
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f'Label {self.index} clicked')
            self.opacity_effect.setOpacity(0.4)
            self.setGraphicsEffect(self.opacity_effect)
            # Emit the clicked signal with the label index
            self.clicked.emit(self.index)

        return super().mouseReleaseEvent(event)



class AppButtons(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        for i in range(2):  # For example, create 3 labels
            #label = QLabel(f'Label {i+1}', self)
            button = AppButton(i+1, f'Label {i+1}', self)
            button.setFixedSize(250, 250)

            # Connect the clicked signal to the deleteAppLabelWidget slot
            # button.clicked.connect(parent.deleteAppLabelWidget)

            self.vlayout.addWidget(button)
            print(button.size().width(), button.size().height())

        self.vlayout.addStretch()
        # create a horizontal layout and add stretch so everything is 
        # pushed to the right

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())



class AppWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        appLabelLayout = QHBoxLayout()
        appLabelLayout.setContentsMargins(50, 50, 50, 50)  # Set all margins to 50
        appLabelLayout.addStretch()

        # Create a button for show and hide the appLabel
        self.btn = HoverButton("<", self)
        appLabelLayout.addWidget(self.btn)
        self.btn.clicked.connect(lambda: self.showAppLabel(self.appLabel))

        self.appLabel = AppButtons(self)
        appLabelLayout.addWidget(self.appLabel)

        # Create a widget for the appLabel layout
        self.appLabelWidget = QWidget(self)
        self.appLabelWidget.setLayout(appLabelLayout)
        self.appLabelWidget.setStyleSheet("background-color: transparent;")

        self.appLabel.hide()


    def showAppLabel(self, appLabel):
        if self.btn.text() == "<":
            self.btn.setText(">")
            appLabel.show()
        else:
            self.btn.setText("<")
            appLabel.hide()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.btn.setText("<")
            self.appLabel.hide()
        return super().mousePressEvent(event)
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.btn.setText(">")
            self.appLabel.show()
        return super().mouseReleaseEvent(event)