import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget

class Avatar(QWidget):
    def __init__(self, width, height, parent=None):
        self.width = width
        self.height = height
    
    def process(self, joint_pos_dict):
        # 1. extract center
        self.center = self.extract_center(joint_pos_dict)
        # 2. draw avatar img
        img = self.drawimg(joint_pos_dict)
        # 3. crop center
        img = self.cropCenter(img)
        return img
    
    def drawimg(self, joint_pos_dict):
        img = np.zeros((self.height, self.width, 3), np.uint8) + 255 #배경 흰색
        for parts in connect_point:
            for i in range(len(parts)-1):
                p = info_dict[parts[i]]
                q = info_dict[parts[i+1]]
                cv2.line(img, (int(joint_pos_dict[p].x * self.width), 
                               int(joint_pos_dict[p].y * self.height)), 
                               (int(joint_pos_dict[q].x * self.width), 
                                int(joint_pos_dict[q].y * self.height)), (0, 0, 0), 5)
        return img

    def extract_center(self, joint_pos_dict):
        center = np.zeros(2)
        center += np.array([joint_pos_dict['LEFT_SHOULDER'].x, joint_pos_dict['LEFT_SHOULDER'].y])
        center += np.array([joint_pos_dict['RIGHT_SHOULDER'].x, joint_pos_dict['RIGHT_SHOULDER'].y])
        center /= 2
        return center

    def cropCenter(self, img):
        x = int(self.center[0] * self.width)
        y = int(self.center[1] * self.height)
        print("center:{}".format(x))
        # img = img[y - int(self.height / 4):y + int(self.height / 4),
        #           x - int(self.width / 4):x + int(self.width / 4), :]
        left = x - int(self.width / 4)
        right = x + int(self.width / 4)

        img = img[:, left:right, :]
        return img

connect_point = [
    [1,2,3], #왼쪽다리
    [6,7,8], #오른쪽다리
    [14,15,16], #왼쪽팔
    [19,20,21], # 오른쪽팔
    [1,6,19,14,1],
    [28,26,24,25,27]
]# 눈코입] #몸통

info_dict = {
    1 : "LEFT_HIP", #left_hip
    2 : "LEFT_KNEE", #left_knee
    3 : "LEFT_ANKLE", #left_ankle
    6 : "RIGHT_HIP", #right_hip
    7 : "RIGHT_KNEE", #right_knee
    8 : "RIGHT_ANKLE", #right_ankle
    14 : "LEFT_SHOULDER", #left_shoulder
    15 : "LEFT_ELBOW", #left_elbow
    16 : "LEFT_WRIST", #left_wrist
    19 : "RIGHT_SHOULDER", #right_shoulder
    20 : "RIGHT_ELBOW", #right_elbow
    21 : "RIGHT_WRIST", #right_wrist
    24 : "NOSE", #nose
    25 : "LEFT_EYE", #left_eye
    26 : "RIGHT_EYE", #right_eye
    27 : "LEFT_EAR", #left_ear
    28 : "RIGHT_EAR" #right_ear
}