from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

import sys

appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence

class MainWindow(QMainWindow):
    def closeEvent(self, e):
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

text = QPlainTextEdit()
window = MainWindow()
window.setCentralWidget(text)

file_path = None

menu = window.menuBar().addMenu("&File")
open_action = QAction("&Open")
def open_file():
    global file_path
    path = QFileDialog.getOpenFileName(window, "Open")[0]
    if path:
        text.setPlainText(open(path).read())
        file_path = path
open_action.triggered.connect(open_file)
open_action.setShortcut(QKeySequence.Open)
menu.addAction(open_action)

save_action = QAction("&Save")
def save():
    if file_path is None:
        save_as()
    else:
        with open(file_path, "w") as f:
            f.write(text.toPlainText())
        text.document().setModified(False)
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
menu.addAction(save_action)

save_as_action = QAction("Save &As...")
def save_as():
    global file_path
    path = QFileDialog.getSaveFileName(window, "Save As")[0]
    if path:
        file_path = path
        save()
save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)

close = QAction("&Close")
close.triggered.connect(window.close)
menu.addAction(close)

help_menu = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
help_menu.addAction(about_action)
def show_about_dialog():
    text = "<center>" \
       "<h1>Text Editor</h1>" \
       "&#8291;" \
       "<img src=\"%s\">" \
       "</center>" \
       "<p>Version 31.4.159.265358<br/>" \
       "Copyright &copy; Company Inc.</p>" \
       % appctxt.get_resource("icon.svg")
    about_dialog = QMessageBox(window)
    about_dialog.setText(text)
    about_dialog.exec_()
about_action.triggered.connect(show_about_dialog)

window.show()

exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
sys.exit(exit_code)
