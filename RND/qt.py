import os, sys, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication
import mediapipe as mp
import cv2

class HandTrackingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.video_label)
        self.hand_landmarker = self.initialize_hand_landmarker()
        self.camera = cv2.VideoCapture(0)
        self.screen_geometry = QGuiApplication.primaryScreen().geometry()

    def initialize_hand_landmarker(self):
        cwd = os.getcwd()
        model_path = os.path.join(cwd, 'RND', 'hand_landmarker.task')
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.print_result
        )
        return mp.tasks.vision.HandLandmarker.create_from_options(options)

    def print_result(self, result, output_image, timestamp_ms):
        if result.hand_landmarks:
            x = self.screen_geometry.x() + result.hand_landmarks[0][0].x * output_image.width
            y = self.screen_geometry.y() + result.hand_landmarks[0][0].y * output_image.height
            QCursor.setPos(x, y)
            QGuiApplication.processEvents()

    def start_video(self):
        while True:
            ret, frame = self.camera.read()
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
            frame_timestamp_ms = int(1000 * time.time())
            self.hand_landmarker.detect_async(mp_image, frame_timestamp_ms)

            h, w, c = frame.shape
            q_image = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

            if cv2.waitKey(1) == ord('q'):
                break

        self.camera.release()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = HandTrackingWidget()
        self.setCentralWidget(self.central_widget)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Hand Tracking with PyQt')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
