import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
from io import BytesIO

class ExerciseResultWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("운동 결과 화면")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 그래프 이미지 생성
        graph_image = self.generate_graph()
        graph_label = QLabel(self)
        graph_label.setPixmap(graph_image)
        layout.addWidget(graph_label)

        # 운동 정보
        exercise_info_label = QLabel("운동 정보")
        layout.addWidget(exercise_info_label)

        exercise_name_label = QLabel("운동 이름: 스쿼트")
        layout.addWidget(exercise_name_label)

        date_label = QLabel("날짜: 2023-12-08")
        layout.addWidget(date_label)

        person_name_label = QLabel("사람 이름: 홍길동")
        layout.addWidget(person_name_label)

        time_label = QLabel("시간: 30분")
        layout.addWidget(time_label)

    def generate_graph(self):
        # Matplotlib을 사용하여 간단한 그래프 생성
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 2])

        # 그래프를 이미지로 변환
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close(fig)

        # 이미지를 QPixmap으로 변환하여 반환
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExerciseResultWindow()
    window.show()
    sys.exit(app.exec())
