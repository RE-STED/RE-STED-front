import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication
from PyQt6.QtCore import QThread, Qt, pyqtSignal
import mediapipe as mp
import cv2, time


class Thread(QThread):
    changePixmap = pyqtSignal(QImage, int, int)

    def __init__(self, size, hand_landmarker):
        super().__init__()
        self.hand_landmarker = hand_landmarker
        self.size = size

    def run(self):
        camera = cv2.VideoCapture(0)
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
    def __init__(self):
        super().__init__()
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
            QCursor.setPos(x, y)
            QGuiApplication.processEvents()

    def setImage(self, image, height, width):
        self.video_label.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width

    def start_video(self):
        self.thread = Thread(self.size(), self.hand_landmarker)
        self.thread.changePixmap.connect(self.setImage)
        self.thread.start()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getFullScreen()
        self.setStyleSheet("background-color: black;")  # Set background color to grey
        self.central_widget = HandTrackingWidget()
        #self.central_widget.resize(QGuiApplication.primaryScreen().geometry())
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Hand Tracking with PyQt')

    def getFullScreen(self):
        screen = QApplication.primaryScreen()
        self.showFullScreen()
        screen_geometry = screen.availableGeometry()

        # 전체 화면으로 윈도우를 설정
        print(QApplication.primaryScreen().size().width(), QApplication.primaryScreen().size().height())
        print(screen_geometry.width(), screen_geometry.height())
        self.setGeometry(screen_geometry)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
