import cv2
import time
import random
import numpy as np
import mediapipe as mp
from mediapipe import ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap

from ..qt6.detectionQT import DetectionWidget

'''
https://github.com/googlesamples/mediapipe/blob/main/examples/object_detection/python/object_detector.ipynb
https://mediapipe-studio.webapps.google.com/studio/demo/object_detector
'''

MARGIN = 5  # pixels
ROW_SIZE = 5  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


label_size = [1470, 890]
label_ratio = label_size[0] / label_size[1]

class Detection:
  """A class to represent a detection result.
  Attributes:
    bounding_box: The bounding box of the detected object.
    categories: The list of categories of the detected object.
  """

  def __init__(self):
    
    base_options = python.BaseOptions(model_asset_path="src/mind/model/od/efficientdet_lite0.tflite")
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                          score_threshold=0.4,
                                          max_results=10,
                                          category_denylist = ['person', 'chair', 'couch'])
    
    self.model = vision.ObjectDetector.create_from_options(options)
    
    
  def visualize(self,
      image,
      detection_result
  ) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualize.
    Returns:
      Image with bounding boxes.
    """
    for detection in detection_result.detections:
      # Draw bounding_box
      bbox = detection.bounding_box
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

      # Draw label and score
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (MARGIN + bbox.origin_x,
                      MARGIN + ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image


  def detect(self, image_np, image_name=None):
    """Detects objects in the input image.
    Args:
      image: The input RGB image.
    Returns:
      The list of all "Detection" entities.
    """
    # Convert the BGR image to RGB and process it with MediaPipe Object detection.
    
    image_mp = mp.Image(image_format=ImageFormat.SRGB, data=image_np)
    detection_result = self.model.detect(image_mp)

    
    image_copy = np.copy(image_mp.numpy_view())
    annotated_image = self.visualize(image_copy, detection_result)
    #cv2.imwrite(image_name, annotated_image)

    
    return detection_result.detections
  
  

# 물건 퀴즈 클래스
class ObjectQuiz(QThread):
  frameCaptured = pyqtSignal(QImage)
  
  def __init__(self, cam):
    super().__init__()
    
    # 영상 속성
    self.Cam = cam
    self.cap = self.Cam.cam
    self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
    self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    
    # 글자 속성
    self.text_color = {'red': (0, 0, 255),
                       'green': (0, 255, 0),
                       'blue': (255, 0, 0),
                       'white': (255, 255, 255),
                       'black': (0, 0, 0),
                       'evergreen':(163, 204, 163)}
    self.thickness = 3
    self.position = {'right_top': (self.width - 200, 50),
                     'right_bottom': (self.width - 200, self.height - 50),
                     'left_top': (50, 50),
                     'left_bottom': (50, self.height - 50),
                     'center': (int(self.width / 2), int(self.height / 2))}
    self.font_scale = 1.5
    self.font_face = cv2.FONT_HERSHEY_DUPLEX

    # Detector
    self.model = Detection()
    
    self.steps = ['']

    
  def run(self):

    window_name = 'MediaPipe Object Detection'

    # 웹캠이 정상적으로 열렸는지 확인
    if not self.cap.isOpened():
        print("Cannot open camera")
        exit()
        
    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
      
    self.show_text("Start Object Quiz!", 3)
    
    self.show_text("Kimchi~", 1)
    
    self.countdown(5, show_window=True)
    
    frame1 = self.show_box(1)
    
    self.show_text("Completed Screenshot", 2)
    
    detections = self.model.detect(frame1, "origin.jpg")
    
    categories = [detection.categories[0].category_name for detection in detections]
    
    while not len(categories):
      self.show_text("Nothing Detected!!", 4)
      print("Wrong!")
      
      self.show_text("Let's try again!", 4)
      
      self.countdown(3, show_window=True)
      
      self.show_text("Kimchi~", 1)
      frame1 = self.show_box(1)
      detections = self.model.detect(frame1, "origin.jpg")
      categories = [detection.categories[0].category_name for detection in detections]
  
    
    target_obj = random.choice(categories)
    
    self.show_text(f"Find {target_obj} in 10 seconds!", 5)

    self.countdown(10, show_window=True)
    
    frame2 = self.show_box(1)
    detection_results = self.model.detect(frame2, "result.jpg")
    
    detection_results = [detection.categories[0].category_name for detection in detection_results]
    
    if len(detection_results) == 0:
      self.show_text("Nothing Detected!!", 3)
      print("Nothing !")
      
    else:
      detection_result = detection_results[0]
      print("\nDetect {}, Answer is {}\n".format(detection_result, target_obj))
      if detection_result == target_obj:
        self.show_text("Correct!", 3)
        print("Correct!")
      else:
        self.show_text("Wrong!", 3)
        print("Wrong!")
      
    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    self.parent.parent.btnWidget.show()
    self.parent.parent.layout.removeWidget(self.parent)
    self.parent.close_window()

    
  
  def get_frame(self):
    frame = self.Cam.capture()
    
    # original_width = frame.shape[1]
    # original_height = frame.shape[0]
    # origin_ratio = frame.shape[1] / frame.shape[0]
    
    # # 원본 프레임과 레이블의 비율을 비교하여 크롭할 부분의 크기 결정
    # if origin_ratio > label_ratio:
    #   new_width = int(original_height * label_ratio)
    #   new_height = original_height
    # else:
    #   new_width = original_width
    #   new_height = int(original_width / label_ratio)

    # # 크롭할 부분의 중심이 원본 프레임의 중심이 되도록 크롭
    # crop_x = (original_width - new_width) // 2
    # crop_y = (original_height - new_height) // 2
    
    # #frame = frame[crop_y : crop_y + new_height, crop_x : crop_x + new_width, :]

    # # 크롭한 프레임을 레이블의 크기로 리사이즈
    # frame = cv2.resize(frame, label_size)
    # self.width = frame.shape[1]
    # self.height = frame.shape[0]
    
    # self.position = {'right_top': (self.width - 200, 50),
    #               'right_bottom': (self.width - 200, self.height - 50),
    #               'left_top': (50, 50),
    #               'left_bottom': (50, self.height - 50),
    #               'center': (int(self.width / 2), int(self.height / 2))}
    
    return frame

  def update_frame(self, frame):
    
    

    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  

    image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)

    self.frameCaptured.emit(image)
    
  # N초 동안 frame을 detection하여 결과를 visulaize한 이미지를 반환하는 함수
  def show_detection(self, show_time):
    start_time = time.time()
    show_over = False

    while True:
        
      if show_over:
          break
    
      input_frame = self.get_frame()
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      #input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
      
      elapsed_time = int(time.time() - start_time)
      remaining_time = max(show_time - elapsed_time, 0)

      output_frame = input_frame.copy()
      detection_result = self.model.detect(output_frame)
      annotated_image = self.model.visualize(output_frame, detection_result)
      
      if remaining_time <= 0:
          show_over = True
          
      #cv2.imshow(window_name, annotated_image)
      self.update_frame(frame=annotated_image)
      
    return annotated_image

  # 영상에 글자를 쓰는 함수
  def draw_text(self, frame, text, position, font_scale=1.0, color=(0, 0, 0), thickness=1):
    
    pos_x, pos_y = position[0] - len(text) * 15, position[1]
    
    return cv2.putText(img=frame,
                        text=text,
                        org=(pos_x, pos_y),
                        fontFace=self.font_face,
                        fontScale=font_scale,
                        color=color,
                        thickness=thickness)

  # 영상에 n초 카운트다운하는 함수
  def countdown(self, countdown_time, show_window = False, window_name='MediaPipe Object Detection'):
    start_time = time.time()
    countdown_over = False

    while True:
        
      if countdown_over:
          break
    
      input_frame = self.get_frame()
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      #input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
      
      elapsed_time = int(time.time() - start_time)
      remaining_time = max(countdown_time - elapsed_time, 0)

      if show_window:
        output_frame = input_frame.copy()
        frame = self.draw_text(frame = output_frame, 
                          text = f"Countdown: {remaining_time}", 
                          position= self.position.get('center'), 
                          font_scale= self.font_scale, 
                          color= self.text_color['blue'], 
                          thickness= self.thickness)
          
      else:
        frame = input_frame

      if remaining_time <= 0:
          countdown_over = True
          
      #cv2.imshow(window_name, frame)
      self.update_frame(frame=frame)
        
  # n초 동안 영상에 글자를 쓰는 함수
  def show_text(self, text, show_time, window_name='MediaPipe Object Detection'):
    start_time = time.time()
    show_over = False

    while True:
        
      if show_over:
          break
    
      input_frame = self.get_frame()
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      #input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
      
      elapsed_time = int(time.time() - start_time)
      remaining_time = max(show_time - elapsed_time, 0)

      output_frame = input_frame.copy()
      frame = self.draw_text(frame = output_frame, 
                          text = text, 
                          position= self.position.get('center'), 
                          font_scale= self.font_scale, 
                          color= self.text_color['blue'], 
                          thickness= self.thickness)

      if remaining_time <= 0:
          show_over = True
          
      #cv2.imshow(window_name, frame)
      self.update_frame(frame=frame)
        
  # 영상 가장자리에 n초동안 흰색 테두리를 만드는 함수
  def show_box(self, show_time, window_name='MediaPipe Object Detection'):
    start_time = time.time()
    show_over = False

    while True:
        
      if show_over:
          break
    
      input_frame = self.get_frame()
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      #input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
      
      elapsed_time = int(time.time() - start_time)
      remaining_time = max(show_time - elapsed_time, 0)

      output_frame = input_frame.copy()
      frame = cv2.rectangle(output_frame, (0, 0), (self.width, self.height), self.text_color['white'], 10)

      if remaining_time <= 0:
          show_over = True
          
      #cv2.imshow(window_name, frame)
      self.update_frame(frame=frame)
      
    return frame

class ObjectWidget(DetectionWidget):
    def __init__(self, cam):
        super().__init__()
        
        self.resize(1920, 1080)
        self.video_size = self.video.size()

        self.captureThread = ObjectQuiz(cam)
        self.captureThread.frameCaptured.connect(self.update_frame)
        
        self.HomeButton.clicked.connect(self.close_window)
        self.HomeButton.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 48pt; color: white; border-radius: 1.5em;} QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 50pt;}");

        self.captureThread.parent = self

    def update_frame(self, image):
        # Convert the QImage to QPixmap and show it on the QLabel\
          
        pixmap = QPixmap.fromImage(image).scaled(self.video_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.video.setPixmap(pixmap)
        
    def close_window(self):
        for i in range(100):
            i = i / 100
            self.setWindowOpacity(1 - i)
            time.sleep(0.005)
        self.close()
        