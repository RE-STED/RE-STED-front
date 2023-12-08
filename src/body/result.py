import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
from io import BytesIO
from guide import PoseGuide

class ExerciseResult(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("운동 결과 화면")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.Guide = PoseGuide(data=data)

        self.setWindowTitle("운동 결과 화면")

        layout = QVBoxLayout(central_widget)

        # 그래프 이미지 생성
        graph_image = self.generate_graph()
        graph_label = QLabel(self)
        graph_label.setPixmap(graph_image)
        layout.addWidget(graph_label)

        # 운동 정보
        exercise_info_label = QLabel("재활 운동 정보")
        layout.addWidget(exercise_info_label)

        exercise_name_label = QLabel(f"운동 이름: {result['joint_name']}")
        layout.addWidget(exercise_name_label)

        date_label = QLabel(f"날짜: {result['date']}")
        layout.addWidget(date_label)

        person_name_label = QLabel(f"사용자 이름: {result['person_name']}")
        layout.addWidget(person_name_label)

        time_label = QLabel(f"운동 시간: {result['time']}")
        layout.addWidget(time_label)

    def generate_graph(self):
        # Matplotlib을 사용하여 간단한 그래프 생성
        file = self.Guide.loadJson(json_adress)
        angle_records = file['angle_records']
        fig = self.Guide.plotAngle(angle_records, json_adress)

        # 그래프를 이미지로 변환
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close(fig)

        # 이미지를 QPixmap으로 변환하여 반환
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        return pixmap

result = {
    "joint_name": "RIGHT_SHOULDER",
    "date": "2023-12-08",
    "person_name": "이용빈",
    "max_angle": "90도",
    "time": "10min",
    "graph": "그래프 이미지"
}

data = {"joint_name": "RIGHT_SHOULDER",
                    'level': 6,
                    'challenge': 10}

json_adress = f'data/Json/RIGHT_SHOULDER/C10L6.json'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExerciseResult()
    window.show()
    sys.exit(app.exec())