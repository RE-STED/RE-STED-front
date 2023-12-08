import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from gesture.gesture import GestureWidget
from menu.appwidget import AppWidget
from menu.bodywidget import PhysicalRehabWidget
from menu.mindwidget import CognitiveRehabWidget
from cam import Cam

# from body.gui import PoseGUI
# from body.gui import PoseGUI
# from body.main2 import PoseGUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cam = Cam()
        self.setWindowTitle('Hand Tracking with PyQt')
        self.getFullScreen()
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        self.handTrackWidget = GestureWidget(self, self.cam)

        
        # Create a stacked layout and add the widgets
        self.layout = QStackedLayout()
        self.layout.addWidget(self.handTrackWidget)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.hideMouseCursor()

        #self.layout.setCurrentWidget(self.appLabel)
        self.addAppLabelWidget()
        #self.addBodyWidget()

        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        
        self.appLabelWidget.appLabel.connectButtonClicked(self.handleButtonClicked)
        

    def getFullScreen(self):
        self.showFullScreen()


    def addAppLabelWidget(self):
        self.appLabelWidget = AppWidget(self)
        self.layout.addWidget(self.appLabelWidget)
        self.layout.setCurrentWidget(self.appLabelWidget)


    def hideMouseCursor(self):
        central_widget = self.centralWidget()
        if isinstance(central_widget, QWidget):
            central_widget.setCursor(Qt.CursorShape.BlankCursor)


    def showMouseCursor(self):
        central_widget = self.centralWidget()
        if isinstance(central_widget, QWidget):
            central_widget.unsetCursor()


    # AppButton이 클릭될 때 실행되는 슬롯
    def handleButtonClicked(self, button_index):
        if button_index == 0:
            self.addPysicalRehabWidget()
        elif button_index == 1:
            self.addCognitiveRehabWidget()
    
    def deleteAppLabelWidget(self, label_index):
        print(f"Deleting AppLabelWidget triggered by Label {label_index}")
        self.layout.removeWidget(self.appLabelWidget.appLabelWidget)
        self.appLabelWidget.appLabelWidget.deleteLater()
        self.appLabelWidget.deleteLater()

        
    def addPysicalRehabWidget(self):
        self.appLabelWidget.hide()
        print("addPysicalRehabWidget")
        self.physicalRehabWidget = PhysicalRehabWidget(self, self.cam)
        self.layout.addWidget(self.physicalRehabWidget)
        self.layout.setCurrentWidget(self.physicalRehabWidget)


    def deletePhysicalRehabWidget(self):
        print("deletePhysicalRehabWidget")
        self.layout.removeWidget(self.physicalRehabWidget)
        self.physicalRehabWidget.deleteLater()
        self.appLabelWidget.show()
        self.layout.setCurrentWidget(self.appLabelWidget)
    
    
    def addCognitiveRehabWidget(self):
        self.appLabelWidget.hide()
        self.appLabelWidget.hide()
        print("addCognitiveRehabWidget")
        self.cognitiveRehabWidget = CognitiveRehabWidget(parent=self, cam=self.cam)
        self.layout.addWidget(self.cognitiveRehabWidget)
        self.layout.setCurrentWidget(self.cognitiveRehabWidget)

    def deleteCognitiveRehabWidget(self):
        print("deleteCognitiveRehabWidget")
        
        # cognitiveRehabWidget의 Result를 json으로 저장
        with open('src/mind/Result.json', 'w', encoding='utf-8') as f:
            json.dump(self.cognitiveRehabWidget.RecordResultDict, f, indent=4, ensure_ascii=False)
        
        self.layout.removeWidget(self.cognitiveRehabWidget)
        self.cognitiveRehabWidget.deleteLater()
        self.appLabelWidget.show()
        self.layout.setCurrentWidget(self.appLabelWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())