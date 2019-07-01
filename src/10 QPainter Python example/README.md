# QPainter Python example

This example application demonstrates how you can use [`QPainter`](https://doc.qt.io/qt-5/qpainter.html) to perform custom rendering in a widget. It turns the text editor from [example 7](../07%20Qt%20Text%20Editor) into an action shooter: When you click inside the editor with the mouse, bullet holes appear.

<p align="center"><img src="../screenshots/qpainter-python-example.png" alt="QPainter Python Example"></p>

The crucial steps of this example are to [override `mousePressEvent(...)`](main.py#L13-L17) to handle the user's clicks, and [`paintEvent(...)`](main.py#L18-L22) to draw the bullets. See the top of [`main.py`](main.py) for how these features work in detail.

To run this example yourself, please follow [these instructions](../../README.md#running-the-examples).
