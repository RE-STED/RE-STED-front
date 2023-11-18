from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.showFullScreen()
        self.central = QWidget()

        # create a vertical layout and add stretch so it is the first
        # item of the layout and everything that is inserted after
        # is pushed down to the bottom
        self.layout = QVBoxLayout(self.central)
        self.layout.addStretch()
       
        self.btn1 = QPushButton("PushButton", self)
        self.btn2 = QPushButton("PushButton", self)
        self.btn3 = QPushButton("PushButton", self)

        # create a horizontal layout and add stretch so everything is 
        # pushed to the right
        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()

        # add buttons after the stretch so they will be pushed to the 
        # right
        self.hlayout.addWidget(self.btn1)
        self.hlayout.addWidget(self.btn2)
        self.hlayout.addWidget(self.btn3)

        # add horizontal layout to vertical layout which will be pushed
        # to the bottom from the vertical layouts stretch
        self.layout.addLayout(self.hlayout)
        #self.layout.addStretch()
        self.setCentralWidget(self.central)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()