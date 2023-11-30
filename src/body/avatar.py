import cv2
import numpy as np
import parameter as pm
from PyQt6.QtWidgets import QWidget

class Avatar(QWidget):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.connect_point = [
                [1,2,3], #왼쪽다리
                [6,7,8], #오른쪽다리
                [14,15,16], #왼쪽팔
                [19,20,21], # 오른쪽팔
                [1,6,19,14,1],
                [28,26,24,25,27]
                ]# 눈코입] #몸통
        self.info_dict = {
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
        
    def drawimg(self, save=False):
        img = np.zeros([self.height,self.width, 3])+255
        for parts in self.connect_point:
            for i in range(len(parts)-1):
                p = self.info_dict[parts[i]]
                q = self.info_dict[parts[i+1]]
                cv2.line(img, (int(pm.joint_pos_dict[p].x * self.width), int(pm.joint_pos_dict[p].y * self.height)), (int(pm.joint_pos_dict[q].x * self.width), int(pm.joint_pos_dict[q].y * self.height)), (245, 66, 230), 5)
        return img