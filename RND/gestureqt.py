import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication, QMouseEvent
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QCoreApplication, QEvent
import mediapipe as mp
import cv2, time, statistics
from collections import deque, Counter
import pymouse

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, int, int)

    def __init__(self, size, gesture_recognizer):
        super().__init__()
        self.gesture_recognizer = gesture_recognizer
        self.size = size
        self.Cam = Cam()

    def run(self):
        while True:
            # ret, frame = camera.read()
            if 1:
                # https://stackoverflow.com/a/55468544/6622587
                frame = self.Cam.capture()
                h, w, ch = frame.shape
                bytesPerLine = ch * w

                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
                #print(self.size.width(), self.size.height())
                scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(),
                                             Qt.TransformationMode.FastTransformation)
                
                self.changePixmap.emit(scaledImage, scaledImage.width(), scaledImage.height())

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                frame_timestamp_ms = int(1000 * time.time())
                self.gesture_recognizer.recognize_async(mp_image, frame_timestamp_ms)


class Cam():
    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        
    def capture(self):
        ret, frame = self.cam.read()
        if ret:
            # color change
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # flip
            img = cv2.flip(img, 1)
            return img
            

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
        
        self.gesture_recognizer = self.initialize_gesture_recognizer()
        self.prev_5_gesture_queue = deque(maxlen=5)
        self.start_video()


    def initialize_gesture_recognizer(self):
        cwd = os.getcwd()
        model_path = os.path.join(cwd, 'RND', 'gesture_recognizer (4).task')
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.moveCursor
        )
        return mp.tasks.vision.GestureRecognizer.create_from_options(options)


    def moveCursor(self, result, output_image, timestamp_ms):
        if result.hand_landmarks:
            # point is relative to the image size + widget absolute position
            x = statistics.mean([result.hand_landmarks[0][0].x * self.image_height, 
                                 result.hand_landmarks[0][3].x * self.image_height, 
                                 result.hand_landmarks[0][9].x * self.image_height, 
                                 result.hand_landmarks[0][17].x * self.image_height]) + self.screen_geometry.x() + self.mapToGlobal(self.video_label.pos()).x()
            y = statistics.mean([result.hand_landmarks[0][0].y * self.image_width,
                                 result.hand_landmarks[0][9].y * self.image_width, 
                                 result.hand_landmarks[0][3].y * self.image_width, 
                                 result.hand_landmarks[0][17].y * self.image_width]) + self.screen_geometry.y() + self.mapToGlobal(self.video_label.pos()).y()
            #print(self.image_height, self.image_width)
            #print(self.screen_geometry.x(), self.screen_geometry.y())
            #print(self.mapToGlobal(self.video_label.pos()).x(), self.mapToGlobal(self.video_label.pos()).y())
            if(result.gestures):
                if(len(result.gestures) > 0):
                    self.prev_5_gesture_queue.append((result.gestures[0][0].category_name, result.gestures[0][0].score))

                    #if prev_5_gesture_queue's the most first element is pinch, then click
                    prev_5_gesture_list = list(self.prev_5_gesture_queue)
                    common_gesture = Counter([value[0] for value in prev_5_gesture_list]).most_common(1)
                    if(common_gesture[0][0] == 'pinch' and common_gesture[0][1] >= 3):
                        #calculate the average score of pinch
                        pinch_score = statistics.mean([value[1] for value in prev_5_gesture_list if value[0] == 'pinch'])
                        if(pinch_score > 0.6):
                            #print("left click", QCursor.pos())
                            # left click
                            pymouse.PyMouse().press(int(x), int(y), 1)
                    else:
                        #print("release click", QCursor.pos())
                        # right click
                        pymouse.PyMouse().release(int(x), int(y), 1)
                    #print(result.gestures[0][0].category_name, result.gestures[0][0].score)

            QCursor.setPos(int(x), int(y))
            QGuiApplication.processEvents()
        
       #print(result)


    def setImage(self, image, height, width):
        self.video_label.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width


    def start_video(self):
        self.thread = Thread(self.size(), self.gesture_recognizer)
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
