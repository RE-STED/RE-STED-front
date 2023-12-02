# from PyQt6.QtWidgets import QWidget
from widget import Pose
import cv2
import numpy as np 
import json
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

from widget import Pose

class PoseGuide():
    def __init__(self, parent=None):
        super().__init__()
        self.video_adress = 'data/video/RIGHT_SHOULDER.mp4'
        self.json_adress = 'data/Json/RIGHT_SHOULDER.json'
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
            landmarks_records.append(self.Pose.convert_to_dict())
            angle_records.append(self.Pose.joint_pos_dict[self.joint].angle)

        data = {'angle_records': angle_records, 'landmarks_records': landmarks_records}
        file = json.dumps(data)

        # JSON 파일에 쓰기
        with open(self.json_adress, 'w') as json_file:
            json_file.write(file)

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

        self.peaks = self.cluster_numbers(peaks, self.threshold)
        self.vallys = self.cluster_numbers(vallys, self.threshold)
        
        self.joint_info = {}
        self.joint_info["peak"] = []
        self.joint_info["vally"] = []

        for cluster in self.peaks:
            middle_index = cluster[int(len(cluster) / 2)]
            self.joint_info["peak"].append({"frame": middle_index, "angle" :self.angle_records[middle_index]})
        for cluster in self.vallys:
            middle_index = cluster[int(len(cluster) / 2)]
            self.joint_info["vally"].append({"frame": middle_index, "angle" :self.angle_records[middle_index]})

        # Amplitude, Period
        amplitude = self.joint_info["peak"][0]['angle'] - self.joint_info["vally"][0]['angle']
        period = self.joint_info["peak"][1]['frame'] - self.joint_info["peak"][0]['frame']

        self.joint_info["amplitude"] = amplitude
        self.joint_info["period"] = period
        print(self.joint_info)

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