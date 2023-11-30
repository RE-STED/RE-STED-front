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
    def __init__(self, cam):
        super().__init__()
        self.running = True
        self.Cam = cam
        self.Pose = Pose()
        self.Avatar = Avatar(1920, 1080)

    def run(self):
        # cam = Cam()
        while self.running:
            # img load
            img = self.Cam.capture() 
            img = cv2.flip(img, 1)

            # img preprocessing & pose landmark detection
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = True
            img, pose_landmarks = self.Pose.pose_detect(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

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

                img = cv2.flip(img, 1)

                # put angle text in image
                cv2.putText(
                    img,
                    str("{}: {}".format("right shoulder", pm.joint_pos_dict["RIGHT_SHOULDER"].angle)),
                    (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                img = cv2.cvtColor(img, cv2.COLOR_BGRRGB)
                # draw avatar
                img = self.Avatar.drawimg()
                img = img.reshape(self.Avatar.height, self.Avatar.width, -1)
            except:
                print('no pose')
            print(img.shape)
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