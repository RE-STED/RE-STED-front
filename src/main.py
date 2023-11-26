from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hand Tracking with PyQt')
        self.getFullScreen()
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        self.handTrackWidget = HandTrackingWidget(self)
        
        # Create a stacked layout and add the widgets
        self.layout = QStackedLayout()
        self.layout.addWidget(self.handTrackWidget)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        #self.layout.setCurrentWidget(self.appLabel)
        self.addAppLabelWidget()
        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        

    def getFullScreen(self):
        self.showFullScreen()


    class HoverButton(QPushButton):
        def __init__(self, text, parent=None):
            super().__init__(text, parent)
            self.defaultSize = QSize(190, 190)
            self.hoverSize = QSize(196, 190)
            self.setStyleSheet("background-color: black; color: white; font-size: 20px; border-radius: 1.5em;")
            self.setMinimumSize(self.defaultSize)
            # Create a QGraphicsOpacityEffect object
            self.opacity_effect = QGraphicsOpacityEffect(self)
            # Set the opacity level. The value should be between 0 (completely transparent) and 1 (completely opaque).
            self.opacity_effect.setOpacity(0.2)
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
                self.opacity_effect.setOpacity(0.6)
                self.setGraphicsEffect(self.opacity_effect)
            return super().mousePressEvent(event)
        
        def mouseReleaseEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.opacity_effect.setOpacity(0.2)
                self.setGraphicsEffect(self.opacity_effect)
            return super().mouseReleaseEvent(event)



    def addAppLabelWidget(self):
        appLabel = AppLabels(self)

        appLabelLayout = QHBoxLayout()
        appLabelLayout.setContentsMargins(50, 50, 50, 50)  # Set all margins to 50
        appLabelLayout.addStretch()
        
        # Create a button for show and hide the appLabel
        self.btn = self.HoverButton("<", self)
        appLabelLayout.addWidget(self.btn)
        self.btn.clicked.connect(lambda: self.showAppLabel(appLabel))

        appLabelLayout.addWidget(appLabel)
        # Create a widget for the appLabel layout
        appLabelWidget = QWidget(self)
        appLabelWidget.setLayout(appLabelLayout)
        appLabelWidget.setStyleSheet("background-color: transparent;")  # Set background color to transparent

        appLabel.hide()
        self.layout.addWidget(appLabelWidget)
        self.layout.setCurrentWidget(appLabelWidget)
    

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