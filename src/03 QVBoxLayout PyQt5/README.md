# QVBoxLayout PyQt5

Layouts let you position GUI elements next to each other. [`QVBoxLayout`](https://doc.qt.io/qt-5/qvboxlayout.html) for instance arranges items vertically:

<p align="center"><img src="../screenshots/qvboxlayout-pyqt5.png" alt="QVBoxLayout PyQt5"></p>

The [source code for this example](main.py) is not much more complex than for our [Hello World app](../01%20PyQt%20QLabel). First, we import PyQt5:

    from PyQt5.QtWidgets import *

Then, we create the required `QApplication`:

    app = QApplication([])

This time, we create a top-level window first. This will act as the container for the two buttons you see in the screenshot:

    window = QWidget()

[`QWidget`](https://doc.qt.io/qt-5/qwidget.html) is the most basic kind of [widget](../02%20PyQt%20Widgets). It would simply be empty if we didn't add any contents to it. (Kind of like a `<div>` element in HTML.).

To tell Qt to arrange our buttons vertically, we create a `QVBoxLayout`:

    layout = QVBoxLayout()

Then, we add the two buttons to it:

    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))

Finally, we add the layout - and thus its contents - to the `window` we created above:

    window.setLayout(layout)

We conclude by showing the window and (as is required) handing control over to Qt:

    window.show()
    app.exec_()

For instructions how you can run this example yourself, please see [here](../../README.md#running-the-examples).

The related [`QHBoxLayout`](https://doc.qt.io/qt-5/qhboxlayout.html) positions items horizontally. For an even more powerful approach, see [`QGridLayout`](https://doc.qt.io/qt-5/qgridlayout.html).
