import numpy as np
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


# ------------------- joint -------------------

joint_pos_dict = {}
joint_speed_dict = {}
joint_direction_dict = {}

current_joint_positions = None
prev_joint_positions = None

firstRun = 0

# ------------------- moving average -------------------
movAvgIndex = 0  # moving average index
movAvgN = 9
speed_buffer = {}
movAvgDict = {}

# record 10 times position information
movAvgDict = {
    "NOSE": [],
    "LEFT_EYE_INNER": [],
    "LEFT_EYE": [],
    "LEFT_EYE_OUTER": [],
    "RIGHT_EYE_INNER": [],
    "RIGHT_EYE": [],
    "RIGHT_EYE_OUTER": [],
    "LEFT_EAR": [],
    "RIGHT_EAR": [],
    "MOUTH_LEFT": [],
    "MOUTH_RIGHT": [],
    "LEFT_SHOULDER": [],
    "RIGHT_SHOULDER": [],
    "LEFT_ELBOW": [],
    "RIGHT_ELBOW": [],
    "LEFT_WRIST": [],
    "RIGHT_WRIST": [],
    "LEFT_PINKY": [],
    "RIGHT_PINKY": [],
    "LEFT_INDEX": [],
    "RIGHT_INDEX": [],
    "LEFT_THUMB": [],
    "RIGHT_THUMB": [],
    "LEFT_HIP": [],
    "RIGHT_HIP": [],
    "LEFT_KNEE": [],
    "RIGHT_KNEE": [],
    "LEFT_ANKLE": [],
    "RIGHT_ANKLE": [],
    "LEFT_HEEL": [],
    "RIGHT_HEEL": [],
    "LEFT_FOOT_INDEX": [],
    "RIGHT_FOOT_INDEX": [],
}

saveAngle = {
    "NOSE": [],
    "LEFT_EYE_INNER": [],
    "LEFT_EYE": [],
    "LEFT_EYE_OUTER": [],
    "RIGHT_EYE_INNER": [],
    "RIGHT_EYE": [],
    "RIGHT_EYE_OUTER": [],
    "LEFT_EAR": [],
    "RIGHT_EAR": [],
    "MOUTH_LEFT": [],
    "MOUTH_RIGHT": [],
    "LEFT_SHOULDER": [],
    "RIGHT_SHOULDER": [],
    "LEFT_ELBOW": [],
    "RIGHT_ELBOW": [],
    "LEFT_WRIST": [],
    "RIGHT_WRIST": [],
    "LEFT_PINKY": [],
    "RIGHT_PINKY": [],
    "LEFT_INDEX": [],
    "RIGHT_INDEX": [],
    "LEFT_THUMB": [],
    "RIGHT_THUMB": [],
    "LEFT_HIP": [],
    "RIGHT_HIP": [],
    "LEFT_KNEE": [],
    "RIGHT_KNEE": [],
    "LEFT_ANKLE": [],
    "RIGHT_ANKLE": [],
    "LEFT_HEEL": [],
    "RIGHT_HEEL": [],
    "LEFT_FOOT_INDEX": [],
    "RIGHT_FOOT_INDEX": [],
}
saveDirection = {
    "NOSE": [],
    "LEFT_EYE_INNER": [],
    "LEFT_EYE": [],
    "LEFT_EYE_OUTER": [],
    "RIGHT_EYE_INNER": [],
    "RIGHT_EYE": [],
    "RIGHT_EYE_OUTER": [],
    "LEFT_EAR": [],
    "RIGHT_EAR": [],
    "MOUTH_LEFT": [],
    "MOUTH_RIGHT": [],
    "LEFT_SHOULDER": [],
    "RIGHT_SHOULDER": [],
    "LEFT_ELBOW": [],
    "RIGHT_ELBOW": [],
    "LEFT_WRIST": [],
    "RIGHT_WRIST": [],
    "LEFT_PINKY": [],
    "RIGHT_PINKY": [],
    "LEFT_INDEX": [],
    "RIGHT_INDEX": [],
    "LEFT_THUMB": [],
    "RIGHT_THUMB": [],
    "LEFT_HIP": [],
    "RIGHT_HIP": [],
    "LEFT_KNEE": [],
    "RIGHT_KNEE": [],
    "LEFT_ANKLE": [],
    "RIGHT_ANKLE": [],
    "LEFT_HEEL": [],
    "RIGHT_HEEL": [],
    "LEFT_FOOT_INDEX": [],
    "RIGHT_FOOT_INDEX": [],
}

class Joint:
    def __init__(self, landmark):
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z
        self.v = landmark.visibility
        self.angle = 0

