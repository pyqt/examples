from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from threadutil import run_in_main_thread
from time import sleep

name = input("Please enter your name: ")
chat_url = "https://build-system.fman.io/chat"
server = Session()

# GUI:
app = QApplication([])
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()

append_message = run_in_main_thread(text_area.appendPlainText)

def fetch_new_messages():
    while True:
        response = server.get(chat_url).text
        if response:
            append_message(response)
        sleep(.5)

def send_message():
    server.post(chat_url, {"name": name, "message": message.text()})
    message.clear()

# Signals:
message.returnPressed.connect(send_message)

thread = Thread(target=fetch_new_messages, daemon=True)
thread.start()

app.exec_()