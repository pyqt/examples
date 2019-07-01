# Qt Designer Python

[Qt Designer](https://build-system.fman.io/qt-designer-download) is a graphical tool for building Qt GUIs:

<p align="center"><img src="../screenshots/qt-designer-windows.png" alt="Qt Designer screenshot on Windows"></p>

It produces `.ui` files. You can load these files from C++ or Python to display the GUI.

The dialog in the following screenshot comes from the file [`dialog.ui`](dialog.ui) in this directory:

<p align="center"><img src="../screenshots/qt-designer-python.png" alt="Qt Designer Python"></p>

The [`main.py`](main.py) script (also in this directory) loads and invokes `dialog.ui` from Python. The steps with which it does this are quite easy.

First, [`main.py`](main.py) imports the `uic` module from PyQt5:

    from PyQt5 import uic

It also imports `QApplication`. Like all (Py)Qt apps, we must create an instance of this class.

    from PyQt5.QtWidgets import QApplication

Then, we use [`uic.loadUiType(...)`](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html#PyQt5.uic.loadUiType) to load the `.ui` file. This returns two classes, which we call `Form` and `Window`:

    Form, Window = uic.loadUiType("dialog.ui")

The first is an ordinary Python class. It has a `.setupUi(...)` method which takes a single parameter, the [widget](../02%20PyQt%20Widgets) in which the UI should be displayed. The type of this parameter is given by the second class, `Window`. This is configured in Qt Designer and is usually one of `QDialog`, `QMainWindow` or `QWidget`.

To show the UI, we thus proceed as follows. First, we create the necessary `QApplication`:

    app = QApplication([])

Then, we instantiate the `Window` class. It will act as the container for our user interface:

    window = Window()

Next, we instantiate the `Form`. We invoke its `.setupUi(...)` method, passing the window as a parameter:

    form = Form()
    form.setupUi(window)

We've now connected the necessary components for displaying the user interface given in the `.ui` file. All that remains is to `.show()` the window and kick off Qt's event processing mechanism:

    window.show()
    app.exec_()

For instructions how to run this example yourself, please see [here](../../README.md#running-the-examples).
