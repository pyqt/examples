# PyQt Signals and Slots

PyQt Signals let you react to user input such as mouse clicks. A *slot* is a function that gets called when such an event occurs. The file [`main.py`](main.py) in this directory shows this in action: When the user clicks a button, a popup appears:

<p align="center"><img src="../screenshots/pyqt-signals-and-slots.jpg" alt="PyQt Signals and Slots"></p>

The code begins in the usual way. First, we import PyQt5 and create a `QApplication`:

    from PyQt5.QtWidgets import *
    app = QApplication([])

Next, we create a button:

    button = QPushButton('Click')

Then we define a function. It will be called when the user clicks the button. You can see that it shows an alert:

    def on_button_clicked():
        alert = QMessageBox()
        alert.setText('You clicked the button!')
        alert.exec_()

And here is where signals and slots come into play: We instruct Qt to invoke our function by _connecting_ it to the `.clicked` signal of our button:

    button.clicked.connect(on_button_clicked)

Finally, we show the button on the screen and hand control over to Qt:

    button.show()
    app.exec_()

For instructions how you can run this example yourself, please see [here](../../README.md#running-the-examples).
