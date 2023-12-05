# from PyQt6.QtWidgets import QWidget
from widget import Pose
import cv2
import numpy as np 
import json
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import math
from PyQt6.QtWidgets import QWidget


from widget import Pose
from avatar import Avatar

class PoseGuide(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        # self.joint_name = self.parent.joint_name
        self.joint_name = "RIGHT_SHOULDER"
        self.video_adress = f'data/video/{self.joint_name}.mp4'
        self.json_adress = f'data/Json/{self.joint_name}/C10L10.json'
        self.Pose = Pose()
        self.Avatar = Avatar(1920, 1080)

        self.challenge = 10
        self.level = 3
        self.guide_adress = f'data/Json/{self.joint_name}/C{self.challenge}L{self.level}.json'

        self.threshold = 15

    def process(self):
        # self.saveVideo(self.video_adress)
        file = self.loadJson(self.json_adress)
        self.angle_records = file['angle_records']
        self.landmarks_records = file['landmarks_records']
        self.length = len(self.angle_records)
        self.featureExtraction(self.angle_records)
        # self.plotAngle()
        self.makeGuide(self.joint_name, challenge=self.challenge, level=self.level)
        # self.playGuide(self.guide_adress)

    # ------------------- json -------------------
    def saveJson(self, data, json_adress):
        file = json.dumps(data)

        # JSON 파일에 쓰기
        with open(json_adress, 'w') as json_file:
            json_file.write(file)
        
    def loadJson(self, json_adress):
        with open(json_adress, 'r') as json_file:
            file = json.load(json_file)
        return file

    def saveVideo(self, video_adress):
        Cam = cv2.VideoCapture(video_adress)
        joint_name = str(video_adress.split('/')[-1].split('.')[0])
        landmarks_records = []
        angle_records = []

        while True:
            ret, frame = Cam.read()
            if not ret:
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.Pose.process(img)
            print(f"frame:{len(landmarks_records)}")
            # save joint info
            landmarks_records.append(self.Pose.convert_to_dict())
            angle_records.append(self.Pose.joint_pos_dict[self.joint_name].angle)
        Cam.release()
        data = {'angle_records': angle_records, 'landmarks_records': landmarks_records, 'challenge': 10, 'level': 10, 'joint_name': joint_name}
        json_adress = f'data/Json/{joint_name}/C10L10.json'
        self.saveJson(data, json_adress)

    def playGuide(self, json_adress):
        with open(json_adress, 'r') as json_file:
            file = json.load(json_file)
            angle_records = file['angle_records']
            landmarks_records = file['landmarks_records']
            length = len(angle_records)
            for i in range(length):
                landmarks_records[i] = self.convert_to_Joint(landmarks_records[i])
                img = self.Avatar.process(landmarks_records[i], joint_name=self.joint_name)
                cv2.imshow('img', img)
                cv2.waitKey(30)
    
    def convert_to_Joint(self, landmarks):
        joint_pos_dict = {}
        for key, landmark in landmarks.items():
            joint_pos_dict[key] = JointDict(landmark)
        return joint_pos_dict
        
    # ------------------- feature extraction -------------------
    def featureExtraction(self, angle_records):
        max_angle = max(angle_records)
        min_angle = min(angle_records)
        middle_angle = (max_angle + min_angle) / 2

        # peaks, vallys
        peaks, _ = find_peaks(angle_records, height=middle_angle)
        vallys, _ = find_peaks((-np.array(angle_records)).tolist(), height=-middle_angle)

        self.peaks = self.cluster_numbers(peaks, self.threshold)
        self.vallys = self.cluster_numbers(vallys, self.threshold)
        
        self.joint_info = {}
        self.joint_info["peak"] = []
        self.joint_info["vally"] = []

        for cluster in self.peaks:
            middle_index = cluster[int(len(cluster) / 2)]
            self.joint_info["peak"].append({"frame": int(middle_index), "angle" :float(angle_records[middle_index])})
        for cluster in self.vallys:
            middle_index = cluster[int(len(cluster) / 2)]
            self.joint_info["vally"].append({"frame": int(middle_index), "angle" :float(angle_records[middle_index])})

        # Amplitude, Period
        amplitude = self.joint_info["peak"][0]['angle'] - self.joint_info["vally"][0]['angle']
        period = self.joint_info["peak"][1]['frame'] - self.joint_info["peak"][0]['frame']

        self.joint_info["amplitude"] = amplitude
        self.joint_info["period"] = period
        # print(self.joint_info)
    
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
    
    # ------------------- Inverse Kinematics -------------------
    def inverse_kinematics(self, A, B, angle_BC, length_BC):
        # B에서 A로 향하는 벡터
        BA_vector = [(A[0] - B[0]), (A[1] - B[1])]

        # BC 벡터의 각도 계산
        angle_BA = math.atan2(BA_vector[1], BA_vector[0])
        
        # BC 벡터의 새로운 각도 계산
        angle_BC_rad = math.radians(angle_BC)
        angle_AC = angle_BA + angle_BC_rad

        # C의 좌표 계산
        C = np.array([B[0] + length_BC * math.cos(angle_AC), B[1] + length_BC * math.sin(angle_AC)])

        return C

    def makeGuide(self, joint_name, challenge=10, level=2):
        # challenge: 운동 단계 수
        # level: 운동 강도
        saveAngle = []
        level_ = level
        frame = len(self.angle_records)

        # ----- parameter -----
        angle_records = self.angle_records
        landmarks_records = self.landmarks_records

        before = 0
        after = frame

        p_idx=0 # peak index
        v_idx=0 # vally index

        peak = self.joint_info['peak']
        vally = self.joint_info['vally']
        coin = 0

        # ----- parameter -----

        if peak[0]['frame'] < vally[0]['frame']:
            before = peak[0]['frame']
            p_idx += 1
            level = challenge - level
        else:
            before = vally[0]['frame']
            v_idx += 1

        start_angle = angle_records[before]

        while(p_idx < len(peak) or v_idx < len(vally)):
            if p_idx >= len(peak) and v_idx >= len(vally):
                break
            elif p_idx >= len(peak):
                after = vally[v_idx]['frame']
                v_idx += 1
            elif v_idx >= len(vally):
                after = peak[p_idx]['frame']
                p_idx += 1
            elif (peak[p_idx]['frame'] <= vally[v_idx]['frame']):
                after = peak[p_idx]['frame']
                p_idx += 1
            elif (peak[p_idx]['frame'] > vally[v_idx]['frame']):
                after = vally[v_idx]['frame']
                v_idx += 1
            # print(f"p_idx -> {p_idx}")
            # print(f"v_idx -> {v_idx}")
            
            if coin % 2 == 0: # even
                end_angle = angle_records[after] / challenge * level 
            else: # odd
                end_angle = angle_records[after]
            
            gap = (end_angle - start_angle) / (after - before)
            # print(f"{before} -> {after}")

            for i in range(before, after):
                angle_records[i] = start_angle + gap * (i - before)
                saveAngle.append(angle_records[i])
                landmarks_records[i][joint_name]['angle'] = angle_records[i]

                joint_A = connected_joints[joint_name][0]
                joint_B = connected_joints[joint_name][1]
                joint_C = connected_joints[joint_name][2]
                joint_D = joint_C
                if len(connected_joints[joint_name]) >= 4:
                    joint_D = connected_joints[joint_name][3]

                A = np.array([landmarks_records[i][joint_A]['x'], landmarks_records[i][joint_A]['y']])
                B = np.array([landmarks_records[i][joint_B]['x'], landmarks_records[i][joint_B]['y']])
                C = np.array([landmarks_records[i][joint_C]['x'], landmarks_records[i][joint_C]['y']])
                D = np.array([landmarks_records[i][joint_D]['x'], landmarks_records[i][joint_D]['y']])

                # CB_length = np.linalg.norm(C - B)
                C_est = self.inverse_kinematics(A, B, angle_records[i], 0.15) + C * 0.02 - D * 0.03
                D_est = self.inverse_kinematics(A, B, angle_records[i], 0.3)
            
                landmarks_records[i][joint_C]['x'] = C_est[0]
                landmarks_records[i][joint_C]['y'] = C_est[1]

                landmarks_records[i][joint_D]['x'] = D_est[0]
                landmarks_records[i][joint_D]['y'] = D_est[1]

            before = after
            start_angle = end_angle
            coin += 1
        # --------- save peak, vally -----------
        for i in range(len(peak)):
            peak[i]['angle'] = angle_records[peak[i]['frame']]
        for i in range(len(vally)):
            vally[i]['angle'] = angle_records[vally[i]['frame']]

        # --------- save Json -----------
        data = {
            'angle_records': angle_records, 
            'landmarks_records': landmarks_records, 
            'challenge': challenge, 
            'level': level_, 
            'joint_name': joint_name,
            'peak': peak,
            'vally': vally,
            }
        json_adress = f'data/Json/{joint_name}/C{challenge}L{level_}.json'
        self.saveJson(data, json_adress)
    
    # ------------------- plot -------------------
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

class JointDict:
    def __init__(self, landmark):
        self.x = landmark['x']
        self.y = landmark['y']
        self.z = landmark['z']
        self.v = landmark['v']
        self.angle = landmark['angle']

connected_joints = {
    "LEFT_KNEE": ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"],
    "LEFT_HIP": ["LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"],
    "LEFT_ANKLE": ["LEFT_KNEE", "LEFT_ANKLE", "LEFT_FOOT_INDEX"],
    "LEFT_ELBOW": ["LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"],
    "LEFT_SHOULDER": ["LEFT_HIP", "LEFT_SHOULDER", "LEFT_ELBOW"],
    "LEFT_WRIST": ["LEFT_ELBOW", "LEFT_WRIST", "LEFT_INDEX"],
    "RIGHT_KNEE": ["RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"],
    "RIGHT_HIP": ["RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"],
    "RIGHT_ANKLE": ["RIGHT_KNEE", "RIGHT_ANKLE", "RIGHT_FOOT_INDEX"],
    "RIGHT_ELBOW": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"],
    "RIGHT_SHOULDER": ["RIGHT_HIP", "RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"],
    "RIGHT_WRIST": ["RIGHT_ELBOW", "RIGHT_WRIST", "RIGHT_INDEX"],
}

length_dict = {"shoulder": 0.15, "elbow": 0.15, "wrist": 0.1, "hip": 0.2, "knee": 0.2, "ankle": 0.1}
length = 0.2

if __name__ == '__main__':
    guide = PoseGuide()
    guide.process()

