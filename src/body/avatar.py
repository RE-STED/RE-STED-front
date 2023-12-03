import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget

class Avatar(QWidget):
    def __init__(self, width, height, parent=None):
        self.width = width
        self.height = height
        # self.joint = self.parent().joint
        self.joint = "RIGHT_SHOULDER"
    
    def process(self, joint_pos_dict, joint=None):
        # 1. extract center
        self.center = self.extract_center(joint_pos_dict)
        # 2. draw avatar img
        img = self.drawimg(joint_pos_dict, joint=joint)
        # 3. crop center
        img = self.cropCenter(img)
        # 4. put angle
        img = self.draw_angle(img, joint_pos_dict, joint=joint)
        return img
    
    def drawimg(self, joint_pos_dict, joint=None):
        img = np.zeros((self.height, self.width, 3), np.uint8) + 255 #배경 흰색

        for parts in connect_point:
            for i in range(len(parts)-1):
                p = info_dict[parts[i]]
                q = info_dict[parts[i+1]]
                cv2.line(img, (int(joint_pos_dict[p].x * self.width), 
                               int(joint_pos_dict[p].y * self.height)), 
                               (int(joint_pos_dict[q].x * self.width), 
                                int(joint_pos_dict[q].y * self.height)), (0, 0, 0), 5)
        if joint is not None:
            for i in range(len(connect_joint[joint])):
                if i == len(connect_joint[joint])-1:
                    break
                A = info_dict[connect_joint[joint][i]]
                B = info_dict[connect_joint[joint][i+1]]
                cv2.line(img, (int(joint_pos_dict[A].x * self.width), 
                               int(joint_pos_dict[A].y * self.height)), 
                               (int(joint_pos_dict[B].x * self.width), 
                                int(joint_pos_dict[B].y * self.height)), (0, 0, 255), 5)
        return img

    def draw_angle(self, img, joint_pos_dict, joint):
        if joint is None:
            return img
        img = cv2.flip(img, 1)
        print(joint_pos_dict[joint].angle)
        # putText -> text font size = 
        cv2.putText(img, "{}".format(int(joint_pos_dict[joint].angle)),
                    (int(self.w * 0.1), int(self.height * 0.2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3, cv2.LINE_AA)
        img = cv2.flip(img, 1)
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
        # print("center:{}".format(x))
        # img = img[y - int(self.height / 4):y + int(self.height / 4),
        #           x - int(self.width / 4):x + int(self.width / 4), :]
        left = x - int(self.width / 4)
        right = x + int(self.width / 4)
        self.w = right - left

        img = img[:, left:right, :]
        return img

connect_point = [
    [1,2,3], #왼쪽다리
    [6,7,8], #오른쪽다리
    [14,15,16], #왼쪽팔
    [19,20,21], #오른쪽팔
    [1,6,19,14,1], #몸통
    [28,26,24,25,27] #얼굴
]

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
connect_joint = {
    "LEFT_HIP" : [1,2,3], #왼쪽다리,
    "LEFT_KNEE" : [2,3],
    "LEFT_ANKLE" : [2,3],
    "RIGHT_HIP" : [6,7,8], #오른쪽다리
    "RIGHT_KNEE" : [7,8],
    "RIGHT_ANKLE" : [7,8],
    "LEFT_SHOULDER" : [14,15,16], #왼쪽팔
    "LEFT_ELBOW" : [15,16],
    "LEFT_WRIST" : [15,16],
    "RIGHT_SHOULDER" : [19,20,21], #오른쪽팔
    "RIGHT_ELBOW" : [20,21],
    "RIGHT_WRIST" : [20,21],
}