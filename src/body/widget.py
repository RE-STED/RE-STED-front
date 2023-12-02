from PyQt6.QtWidgets import QWidget
import cv2, json

import mediapipe as mp
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


# ----------------- Pose -----------------

class Pose(QWidget):
    def __init__(self):
        super().__init__()
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        
        self.joint_pos_dict = {}

    def process(self, img):
        # 1. pose landmark detection
        self.landmarks = self.pose_detect(img)

        # 2. save joint info
        self.get_landmarks()
    
    def pose_detect(self, img): # fin
        img.flags.writeable = False
        self.results = self.pose.process(img)
        img.flags.writeable = True

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        landmarks = self.results.pose_landmarks.landmark
        return landmarks

    def draw_landmarks(self, img): # fin
        self.mp_drawing.draw_landmarks(
            img,
            self.results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )

    def get_landmarks(self):
        # joint_pos_dict에 저장
        for i, landmark in enumerate(self.landmarks):
            self.joint_pos_dict[poseIndex[i]] = Joint(landmark)
        # joint_pos_dict에 저장된 값으로 각도 계산
        for joint in joint_angle_list:
            angle = self.extract_angle(joint)
            self.joint_pos_dict[joint[1]].angle = angle
            print("{}: {}".format(joint[1], int(angle)))


    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
    
    def extract_angle(self, joint):
        a = [self.joint_pos_dict[joint[0]].x, self.joint_pos_dict[joint[0]].y]
        b = [self.joint_pos_dict[joint[1]].x, self.joint_pos_dict[joint[1]].y]
        c = [self.joint_pos_dict[joint[2]].x, self.joint_pos_dict[joint[2]].y]
        return self.calculate_angle(a, b, c)

class Joint:
    def __init__(self, landmark):
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z
        self.v = landmark.visibility
        self.angle = 0

# ----------------- PoseGuide -----------------

class PoseGuide():
    def __init__(self, parent=None):
        super().__init__()
        self.video_adress = 'data/video/RIGHT_SHOULDER.mp4'
        self.json_adress = 'data/Json/right_shoulder.json'
        self.joint = 'RIGHT_SHOULDER'
        self.Pose = Pose()
        self.Cam = cv2.VideoCapture(self.video_adress)
        self.threshold = 15

    def process(self):
        self.saveJson()
        self.loadJson()
        self.featureExtraction()
        self.plotAngle()

    def saveJson(self):
        landmarks_records = []
        angle_records = []
        while True:
            ret, frame = self.Cam.read()
            if not ret:
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.Pose.process(img)

            # save joint info
            landmarks_records.append(self.Pose.joint_pos_dict)
            angle_records.append(self.Pose.joint_pos_dict[self.joint].angle)

        # save json
        file = {'angle_records': angle_records, 'landmarks_records': landmarks_records}
        with open(self.json_adress, 'w') as json_file:
            json.dump(file, json_file)

    def loadJson(self):
        with open(self.json_adress, 'r') as json_file:
            file = json.load(json_file)
            self.angle_records = file['angle_records']
            self.landmarks_records = file['landmarks_records']
            self.length = len(self.angle_records)
    
    def featureExtraction(self):
        max_angle = max(self.angle_records)
        min_angle = min(self.angle_records)
        middle_angle = (max_angle + min_angle) / 2

        # peaks, vallys
        peaks, _ = find_peaks(self.angle_records, height=middle_angle)
        vallys, _ = find_peaks(-np.array(self.angle_records), height=-middle_angle)

        # Amplitude, Period
        self.amplitude = max_angle - min_angle
        self.period = len(self.angle_records) / len(peaks)

        self.peaks = self.cluster_numbers(peaks, self.threshold)
        self.vallys = self.cluster_numbers(vallys, self.threshold)

    def plotAngle(self):
        title = str(self.json_adress.split('/')[-1].split('.')[0])    
        plt.plot(self.angle_records)

        self.plot_clusters(self.peaks, mode='peaks')
        self.plot_clusters(self.vallys, mode='vallys')

        plt.title(title)
        plt.xlabel('Frame')
        plt.ylabel('Angle (degrees)')
        plt.show()

    def plot_clusters(self, clusters, mode='peaks'):
        cluster_colors = ['red', 'green', 'purple', 'orange', 'cyan', 'brown', 'pink', 'gray']
        marker = 'o'
        if mode == 'peaks':
            marker = 'x'
        
        for i, cluster in enumerate(clusters):
            cluster_x = cluster
            cluster_y = [self.angle_records[c] for c in cluster]
            plt.scatter(cluster_x, cluster_y, color=cluster_colors[i], label=f'{mode} {i+1}', marker=marker)
    
    def cluster_numbers(self, numbers, threshold):
        clusters = []
        current_cluster = [numbers[0]]

        for i in range(1, len(numbers)):
            diff = abs(numbers[i] - current_cluster[-1])

            if diff <= threshold:
                current_cluster.append(numbers[i])
            else:
                clusters.append(current_cluster)
                current_cluster = [numbers[i]]

        # 마지막 군집 추가
        clusters.append(current_cluster)

        return clusters

if __name__ == '__main__':
    guide = PoseGuide()
    guide.process()


poseIndex = [
    "NOSE",
    "LEFT_EYE_INNER",
    "LEFT_EYE",
    "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER",
    "RIGHT_EYE",
    "RIGHT_EYE_OUTER",
    "LEFT_EAR",
    "RIGHT_EAR",
    "MOUTH_LEFT",
    "MOUTH_RIGHT",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "LEFT_ELBOW",
    "RIGHT_ELBOW",
    "LEFT_WRIST",
    "RIGHT_WRIST",
    "LEFT_PINKY",
    "RIGHT_PINKY",
    "LEFT_INDEX",
    "RIGHT_INDEX",
    "LEFT_THUMB",
    "RIGHT_THUMB",
    "LEFT_HIP",
    "RIGHT_HIP",
    "LEFT_KNEE",
    "RIGHT_KNEE",
    "LEFT_ANKLE",
    "RIGHT_ANKLE",
    "LEFT_HEEL",
    "RIGHT_HEEL",
    "LEFT_FOOT_INDEX",
    "RIGHT_FOOT_INDEX",
]

# left side
left_knee = ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"]
left_hip = ["LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"]
left_ankle = ["LEFT_KNEE", "LEFT_ANKLE", "LEFT_FOOT_INDEX"]
left_elbow = ["LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"]
left_shoulder = ["LEFT_HIP", "LEFT_SHOULDER", "LEFT_ELBOW"]
left_wrist = ["LEFT_ELBOW", "LEFT_WRIST", "LEFT_INDEX"]

# right side
right_knee = ["RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"]
right_hip = ["RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"]
right_ankle = ["RIGHT_KNEE", "RIGHT_ANKLE", "RIGHT_FOOT_INDEX"]
right_elbow = ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"]
right_shoulder = ["RIGHT_HIP", "RIGHT_SHOULDER", "RIGHT_ELBOW"]
right_wrist = ["RIGHT_ELBOW", "RIGHT_WRIST", "RIGHT_INDEX"]


# ------------------- joint -------------------
joint_angle_list = [left_shoulder, left_elbow, left_wrist, left_hip, left_knee, left_ankle, right_shoulder, right_elbow, right_wrist, right_hip, right_knee, right_ankle] # joint angle information
