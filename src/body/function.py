import numpy as np
import parameter as pm
import function as fn
from scipy.signal import find_peaks

def extract_angle(joint):
    a = [pm.joint_pos_dict[joint[0]].x, pm.joint_pos_dict[joint[0]].y]
    b = [pm.joint_pos_dict[joint[1]].x, pm.joint_pos_dict[joint[1]].y]
    c = [pm.joint_pos_dict[joint[2]].x, pm.joint_pos_dict[joint[2]].y]
    return calculate_angle(a, b, c)

# 코사인 유사도 공식으로 각도 구하기
def calculate_angle(a, b, c):
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

def find_period_amplitude(data):
    # 데이터의 길이를 가져옵니다.
    data_length = len(data)

    # 주기 추정
    autocorrelation = np.correlate(data, data, mode='full') # correlate는 어떤함수? mode는 어떤거? full은 무슨의미? 
    # mode='full'은 두 시계열의 길이가 같지 않을 때, 두 시계열의 길이를 합한 길이의 결과를 반환합니다.
    
    autocorrelation = autocorrelation[data_length - 1:]
    peaks, _ = find_peaks(autocorrelation)
    period_estimate = peaks[0]  # 첫 번째 피크를 주기로 사용

    # 진폭 추정
    amplitude_estimate = np.max(data)

    return period_estimate, amplitude_estimate

# 이동 평균 필터로 관절의 속도와 방향을 계산
#  direction -> up : 1, down : 0 and zero : 0.5
def movAvgFilter(landmarks):
    # 현재 관절 위치 업데이트
    pm.current_joint_positions = np.array([(lm.x, lm.y) for lm in landmarks])

    if pm.prev_joint_positions is not None:
        # 이전 관절 위치와 현재 관절 위치의 차이를 계산하여 속도를 얻습니다.
        joint_speeds = pm.current_joint_positions - pm.prev_joint_positions
        for i, speed in enumerate(joint_speeds):
            # 관절의 속도를 계산합니다.
            pm.movAvgDict[pm.poseIndex[i]].append(speed)
            while len(pm.movAvgDict[pm.poseIndex[i]]) > pm.movAvgN:
                pm.movAvgDict[pm.poseIndex[i]].pop(0)
            pm.joint_speed_dict[pm.poseIndex[i]] = np.mean(
                pm.movAvgDict[pm.poseIndex[i]], axis=0
            )
            # 관절의 방향을 계산합니다.
            direction = [(x < 0, y < 0) for x, y in pm.movAvgDict[pm.poseIndex[i]]]
            pm.joint_direction_dict[pm.poseIndex[i]] = np.median(direction, axis=0)
            pm.saveDirection[pm.poseIndex[i]].append(pm.joint_direction_dict[pm.poseIndex[i]])

    # 현재 관절 위치를 이전 위치로 설정
    pm.prev_joint_positions = pm.current_joint_positions

if __name__ == "__main__":
    print("squart_feedback.py")
    a = [0, 1]
    b = [1, 0]
    c = [1, 0] + [0, 1]
    print(np.abs(90 - calculate_angle(a, b, c)))
