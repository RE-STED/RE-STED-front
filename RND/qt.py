import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QColor
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
import mediapipe as mp
import cv2, time


class Thread(QThread):
    changePixmap = pyqtSignal(QImage, int, int)

    def __init__(self, size, hand_landmarker):
        super().__init__()
        self.hand_landmarker = hand_landmarker
        self.size = size

    def run(self):
        camera = cv2.VideoCapture(1)
        while True:
            ret, frame = camera.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imgRGB = cv2.flip(imgRGB, 1)
                h, w, ch = imgRGB.shape
                bytesPerLine = ch * w

                convertToQtFormat = QImage(imgRGB.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
                #print(self.size.width(), self.size.height())
                scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(),
                                             Qt.TransformationMode.FastTransformation)
                
                self.changePixmap.emit(scaledImage, scaledImage.width(), scaledImage.height())

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
                frame_timestamp_ms = int(1000 * time.time())
                self.hand_landmarker.detect_async(mp_image, frame_timestamp_ms)



class HandTrackingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_geometry = QGuiApplication.primaryScreen().geometry()
        #print("handtrack widget size", self.screen_geometry.width(), self.screen_geometry.height())
 
        self.video_label = QLabel(self)
        self.video_label.resize(self.screen_geometry.width(), self.screen_geometry.height())
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set all margins to 0
        self.layout.addWidget(self.video_label)
        
        self.hand_landmarker = self.initialize_hand_landmarker()
        self.start_video()

    def initialize_hand_landmarker(self):
        cwd = os.getcwd()
        model_path = os.path.join(cwd, 'RND', 'hand_landmarker.task')
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.moveCursor
        )
        return mp.tasks.vision.HandLandmarker.create_from_options(options)

    def moveCursor(self, result, output_image, timestamp_ms):
        if result.hand_landmarks:
            # point is relative to the image size + widget absolute position
            x = result.hand_landmarks[0][0].x * self.image_height + self.screen_geometry.x() + self.mapToGlobal(self.video_label.pos()).x()
            y = result.hand_landmarks[0][0].y * self.image_width + self.screen_geometry.y() + self.mapToGlobal(self.video_label.pos()).y()
            #print(self.image_height, self.image_width)
            #print(self.screen_geometry.x(), self.screen_geometry.y())
            #print(self.mapToGlobal(self.video_label.pos()).x(), self.mapToGlobal(self.video_label.pos()).y())

            QCursor.setPos(int(x), int(y))
            QGuiApplication.processEvents()

    def setImage(self, image, height, width):
        self.video_label.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width

    def start_video(self):
        self.thread = Thread(self.size(), self.hand_landmarker)
        self.thread.changePixmap.connect(self.setImage)
        self.thread.start()



class ClickableLabel(QLabel):
    def __init__(self, index, text, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.5)  # 50% opacity
        self.setGraphicsEffect(self.opacity_effect)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f'Label {self.index} clicked')



class AppLabels(QWidget):
    def __init__(self, parent=None):
        super(AppLabels, self).__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addStretch()

        for i in range(2):  # For example, create 3 labels
            #label = QLabel(f'Label {i+1}', self)
            label = ClickableLabel(i+1, f'Label {i+1}', self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet('background: black; color: white; font-size: 20px; border-radius: 1.5em;')
            label.setFixedSize(250, 250)

            self.vlayout.addWidget(label)
            print(label.size().width(), label.size().height())

        self.vlayout.addStretch()
        # create a horizontal layout and add stretch so everything is 
        # pushed to the right

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
        self.resize(self.sizeHint())



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
            self.defaultSize = QSize(110, 110)
            self.hoverSize = QSize(115, 110)
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
            self.opacity_effect.setOpacity(0.6)
            self.setGraphicsEffect(self.opacity_effect)
            self.animation.setStartValue(self.size())
            self.animation.setEndValue(self.hoverSize)
            self.animation.start()

        def leaveEvent(self, event):
            self.opacity_effect.setOpacity(0.2)
            self.setGraphicsEffect(self.opacity_effect)
            self.animation.setStartValue(self.size())
            self.animation.setEndValue(self.defaultSize)
            self.animation.start()



    def addAppLabelWidget(self):
        appLabel = AppLabels(self)

        appLabelLayout = QHBoxLayout()
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
