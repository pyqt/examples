from PyQt6.QtWidgets import *

app = QApplication([])
button = QPushButton('Click')

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()

button.clicked.connect(on_button_clicked)
button.show()
app.exec()