from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

import cv2
# from body.widget import Pose
from widget import Pose
from avatar import Avatar
import parameter as pm
import function as fn


# ----------------- thread -----------------
# thread1 for pose estimation
class Thread1(QThread):
    updateImg = pyqtSignal(QImage, int, int)
    def __init__(self, cam, parant=None):
        super().__init__()
        self.running = True
        self.Cam = cam
        self.Pose = Pose()
        self.Avatar = Avatar(1920, 1080, parant=self)

    def run(self):
        # cam = Cam()
        while self.running:
            # img load
            img = self.Cam.capture() 
            img = cv2.flip(img, 1)

            # img preprocessing & pose landmark detection
            img, pose_landmarks = self.Pose.pose_detect(img)

            # save joint info
            try:
                for i, landmark in enumerate(pose_landmarks.landmark):
                    pm.joint_pos_dict[pm.poseIndex[i]] = pm.Joint(landmark)

                # save joint angle
                for joint in pm.joint_angle_list:
                    pm.joint_pos_dict[joint[1]].angle = fn.extract_angle(joint)
                    print(joint[2], end =':')
                    print(pm.joint_pos_dict[joint[1]].angle)
                    pm.saveAngle[joint[1]].append(pm.joint_pos_dict[joint[1]].angle)
                print('----------------------------------------------')

                img = self.Avatar.process()
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            except:
                print('no pose')
                            # draw avatar
            # img = self.Avatar.process()
            print(img.shape)
            img = cv2.flip(img, 1)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            

            if ch == 1:
                convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_Grayscale8)
            else:
                convertToQtFormat = QImage(img.data, w, h, w * ch, QImage.Format.Format_RGB888)
            scaledImage = convertToQtFormat.scaledToWidth(QApplication.primaryScreen().size().width(), Qt.TransformationMode.FastTransformation)
            self.updateImg.emit(scaledImage, scaledImage.width(), scaledImage.height())
        
            pm.firstRun = 1

    def on(self):
        self.running = True

    def off(self):
        self.running = False

# thread2 for pygame
class Thread2(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        while self.running:
            pass
    
    def on(self):
        self.running = True
    
    def off(self):
        self.running = False