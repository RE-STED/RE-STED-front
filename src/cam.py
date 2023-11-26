import cv2

class Cam():
    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        
    def capture(self):
        ret, frame = self.cam.read()
        if ret:
            # color change
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # flip
            img = cv2.flip(img, 1)
            return img