from PyQt6.QtGui import QCursor, QGuiApplication
import sys
import time

app = QGuiApplication(sys.argv)
screenGeometry = QGuiApplication.primaryScreen().geometry()

while True:
    x, y = 100, 100
    print("Setting cursor position:", x, y)
    QCursor.setPos(x, y)
    QGuiApplication.processEvents()  # Process Qt events
    print(screenGeometry.x(), screenGeometry.y())q
    time.sleep(2)