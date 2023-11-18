from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os

class AppLabels(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        for i in range(10):  # For example, create 10 labels
            label = QLabel(f'Label {i+1}', self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet('background-color: red; color: white; font-size: 20px;')
            label.setFixedSize(200, 200)
            layout.addWidget(label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screensize = app.primaryScreen().geometry().size()
    ex = AppLabels()
    ex.show()

sys.exit(app.exec())