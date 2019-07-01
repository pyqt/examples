# PyQt QLabel

This example shows how you can create a Hello World app using PyQt. It uses a [`QLabel`](https://doc.qt.io/qt-5/qlabel.html) to display a simple window:

![PyQt QLabel screenshot](../screenshots/pyqt-qlabel.png)

```
from PyQt5.QtWidgets import *
app = QApplication([])
label = QLabel('Hello World!')
label.show()
app.exec_()
```

For instructions how you can run this code, please see the [top-level README](../../README.md#running-the-examples).

The code works as follows: First, we import the necessary PyQt classes via the statement:

    from PyQt5.QtWidgets import *

Next, we create a [`QApplication`](https://doc.qt.io/Qt-5/qapplication.html). This is required in every PyQt app. In a sense, it initializes PyQt:

    app = QApplication([])

Then, we create the label with the text we want:

    label = QLabel('Hello World!')

By calling `.show()` on a [widget](../02%20PyQt%20Widgets), we can spawn a window that displays it:

    label.show()

Finally, we hand control over to Qt:

    app.exec_()

This too is required in every Qt application. It gives Qt a chance to run and process user input, such as for instance when the user clicks the "Window close" button.

And that's it! Congratulations on your first PyQt app :-)
