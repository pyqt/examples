from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWidgets import QApplication

app = QApplication([])
engine = QQmlApplicationEngine()
engine.load("main.qml")
app.exec()