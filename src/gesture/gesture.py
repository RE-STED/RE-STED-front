import os, sys
sys.path.append('src')

from cam import Cam

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QCursor, QGuiApplication
from PyQt6.QtCore import QThread, Qt, pyqtSignal
import mediapipe as mp
import time, statistics
from collections import deque, Counter
import pymouse

class GestureThread(QThread):
    changePixmap = pyqtSignal(QImage, int, int)

    def __init__(self, size, gesture_recognizer, cam=None):
        super().__init__()
        self.gesture_recognizer = gesture_recognizer
        self.size = size
        self.cam = cam

    def run(self):
        while True:
            # ret, frame = camera.read()
            if 1:
                # https://stackoverflow.com/a/55468544/6622587
                frame = self.cam.capture()
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



class GestureWidget(QWidget):


    def __init__(self, parent=None, cam=None):
        super().__init__(parent)
        self.cam = cam
        self.screen_geometry = QGuiApplication.primaryScreen().geometry()
        #print("handtrack widget size", self.screen_geometry.width(), self.screen_geometry.height())
        self.video_label = QLabel(self)
        self.video_label.resize(self.screen_geometry.width(), self.screen_geometry.height())
        self.gesture = None
        self.cursorFlag = False
        self.gesture = None
        self.cursorFlag = False
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set all margins to 0
        self.layout.addWidget(self.video_label)
        
        self.gesture_recognizer = self.initialize_gesture_recognizer()
        self.prev_gesture_queue = deque(maxlen=7)
        self.prev_gesture_queue = deque(maxlen=7)
        self.start_video()


    def initialize_gesture_recognizer(self):
        cwd = os.getcwd()
        model_path = os.path.join(cwd, 'model', 'gesture', 'gesture_recognizer(add_rock).task')
        model_path = os.path.join(cwd, 'model', 'gesture', 'gesture_recognizer(add_rock).task')
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.moveCursor
        )
        return mp.tasks.vision.GestureRecognizer.create_from_options(options)


    def moveCursor(self, result, output_image, timestamp_ms):
        x, y = QCursor.pos().x(), QCursor.pos().y()


        x, y = QCursor.pos().x(), QCursor.pos().y()


        if result.hand_landmarks:
            if hasattr(self, 'image_height') and self.cursorFlag == True:
            # point is relative to the image size + widget absolute position
                x = statistics.mean([result.hand_landmarks[0][0].x * self.image_height, 
                                    result.hand_landmarks[0][3].x * self.image_height, 
                                    result.hand_landmarks[0][9].x * self.image_height, 
                                    result.hand_landmarks[0][17].x * self.image_height]) + self.screen_geometry.x() + self.mapToGlobal(self.video_label.pos()).x()
                y = statistics.mean([result.hand_landmarks[0][0].y * self.image_width,
                                    result.hand_landmarks[0][9].y * self.image_width, 
                                    result.hand_landmarks[0][3].y * self.image_width, 
                                    result.hand_landmarks[0][17].y * self.image_width]) + self.screen_geometry.y() + self.mapToGlobal(self.video_label.pos()).y()
            

        if result.gestures:
            if(len(result.gestures) > 0):
                self.prev_gesture_queue.append((result.gestures[0][0].category_name, result.gestures[0][0].score))

                prev_gesture_list = list(self.prev_gesture_queue)
                common_gesture = Counter([value[0] for value in prev_gesture_list]).most_common(1)
                #print(self.gesture, common_gesture[0][1])

                if common_gesture[0][0] == 'rock' and common_gesture[0][1] >= 5:
                    #calculate the average score of rock
                    rock_score = statistics.mean([value[1] for value in prev_gesture_list if value[0] == 'rock'])
                    if(rock_score > 0.8 and self.gesture != 'rock'):
                        if self.cursorFlag == False:
                            self.cursorFlag = True
                            self.gesture = 'rock'
                            self.window().showMouseCursor()
                            #print("cursor on")
                        
                        else:
                            self.cursorFlag = False
                            self.gesture = 'rock'
                            self.window().hideMouseCursor()
                            #print("cursor off")
                
                elif common_gesture[0][0] == 'palmOn' and common_gesture[0][1] >= 5:
                    #calculate the average score of paper
                    self.gesture = 'palmOn'
                    #print("palmOn")

                elif common_gesture[0][0] == 'pinch':
                    self.gesture = 'pinch'
                    #print("pinch")
                
                else:
                    self.gesture = 'None'
                    #print("None")

                #if prev_gesture_queue has pinch, then click
                if self.cursorFlag == True:
                    if self.gesture == 'pinch':
                        #calculate the average score of pinch
                        pinch_score = statistics.mean([value[1] for value in prev_gesture_list if value[0] == 'pinch'])
                        pinch_score = statistics.mean([value[1] for value in prev_gesture_list if value[0] == 'pinch'])
                        if(pinch_score > 0.6):
                            # left click
                            pymouse.PyMouse().press(int(x), int(y), 1)
                    else:
                        pymouse.PyMouse().release(int(x), int(y), 1)


                #print(result.gestures[0][0].category_name, result.gestures[0][0].score)


                #print(result.gestures[0][0].category_name, result.gestures[0][0].score)

            QCursor.setPos(int(x), int(y))
            QGuiApplication.processEvents()
        
       #print(result)


    def setImage(self, image, height, width):
        self.video_label.setPixmap(QPixmap.fromImage(image))
        self.image_height = height
        self.image_width = width


    def start_video(self):
        self.gesture_thread = GestureThread(self.size(), self.gesture_recognizer, self.cam)
        self.gesture_thread.changePixmap.connect(self.setImage)
        self.gesture_thread.start()
