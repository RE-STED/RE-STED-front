from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

import cv2
# from body.widget import Pose
from widget import Pose
from avatar import Avatar
from guide import PoseGuide
import time

# ----------------- thread -----------------
# thread1 for pose estimation
class Thread1(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self, cam, parent=None):
        super().__init__()
        self.parent = parent
        self.running = True
        # self.joint_name = self.parent.joint_name
        self.joint_name = "RIGHT_SHOULDER"

        self.Cam = cam
        self.Pose = Pose(parent=self)
        self.Avatar = Avatar(1920, 1080, parent=self)
        

    def run(self):
        # cam = Cam()
        while self.running:
            # img load
            img = self.Cam.capture() 
            img = cv2.flip(img, 1)

            # ------ pose estimation ------
            try:
                self.Pose.process(img)
                img = self.Avatar.process(self.Pose.joint_pos_dict, joint_name=self.joint_name)
                img = cv2.flip(img, 1)
                h, w, _ = img.shape
                if w <= 0 or h <= 0:
                    raise Exception
            except:
                print('no pose')
                # init camera pose
                img = self.Cam.capture() 
                h, w, _ = img.shape
                # writing on image in the center red color bigger than cv2.LineAA
                cv2.putText(img, 'Show your face', (int(w/2), int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)

            
            # ------ send img to gui ------
            print(img.shape)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            

            if ch == 1:
                convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_Grayscale8)
            else:
                convertToQtFormat = QImage(img.data, w, h, w * ch, QImage.Format.Format_RGB888)
            scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(), Qt.TransformationMode.FastTransformation)
            self.updateImg.emit(scaledImage, scaledImage.width(), scaledImage.height())

    def on(self):
        self.running = True

    def off(self):
        self.running = False

# thread2 for guide
class Thread2(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.running = True
        # self.joint_name = self.parent.joint_name
        self.joint_name = "RIGHT_SHOULDER"

        # --------- thread1 ------------
        self.thread1 = self.parent.thread1
        self.Pose = self.thread1.Pose
        self.joint_pos_dict = self.Pose.joint_pos_dict
        # ------------------------------

        self.Cam = cv2.VideoCapture(f'data/video/{self.joint_name}.mp4')
        self.Pose = Pose()
        self.Avatar = Avatar(1920, 1080, parent=self)
        self.Guide = PoseGuide(parent=self)
        self.Guide.process()
        self.count = 0

    def run(self):
        while self.running:
            file = self.Guide.loadJson(self.Guide.guide_adress)
            angle_records = file['angle_records']
            landmarks_records = file['landmarks_records']
            length = len(angle_records)
            peak = file['peak']
            vally = file['vally']
            joint_name = file['joint_name']

            p_idx = 0
            v_idx = 0

            for i in range(length):
                if not self.running:
                    print('thread2 break')
                    break
                if p_idx >= len(peak):
                    continue
                if v_idx >= len(vally):
                    continue
                elif i == peak[p_idx]['frame']:
                    while self.joint_pos_dict[joint_name].angle < peak[p_idx]['angle']:
                        time.sleep(1/30)
                        print('peak wait')
                    p_idx += 1
                    self.count += 1
                    print(self.count)

                elif i == vally[v_idx]:
                    print(vally[v_idx]['angle'])
                    while self.joint_pos_dict[joint_name].angle > vally[v_idx]['angle']:
                        time.sleep(1/30)
                        print('vally wait')
                    v_idx += 1

                landmarks = self.Guide.convert_to_Joint(landmarks_records[i])
                img = self.Avatar.process(landmarks, joint_name=joint_name)
                img = cv2.flip(img, 1)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                h, w, _ = img.shape

                # ------ send img to gui ------
                print(img.shape)
                h, w, ch = img.shape
                bytesPerLine = ch * w
                
                time.sleep(1/30)
                
                if ch == 1:
                    convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_Grayscale8)
                else:
                    convertToQtFormat = QImage(img.data, w, h, w * ch, QImage.Format.Format_RGB888)
                scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(), Qt.TransformationMode.FastTransformation)
                self.updateImg.emit(scaledImage, scaledImage.width(), scaledImage.height()) 
    
    def on(self):
        self.running = True
        self.count = 0
    
    def off(self):
        self.running = False