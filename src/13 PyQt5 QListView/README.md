# PyQt5 QListView

This example shows how you can use a PyQt5 [`QListView`](https://doc.qt.io/qt-5/qlistview.html) to display a list.

<p align="center"><img src="../screenshots/pyqt5-qlistview.png" alt="PyQt5 QListView"></p>

It simply shows a static list of strings. Technically, the data is managed by Qt's [`QStringListModel`](https://doc.qt.io/qt-5/qstringlistmodel.html). The important steps of the [code](main.py) are:

```
model = QStringListModel(["An element", "Another element", "Yay! Another one."])
view = QListView()
view.setModel(model)
view.show()
```

This is very similar to the [previous example](../12%20QTreeView%20example%20in%20Python), where we displayed a tree view of files. The reason for this similarity is that both examples use Qt's Model/View framework. As an exercise for yourself, you might want to try using `QListView` instead of `QTreeView` in the previous example.

To run this example, please follow [the instructions in the README of this repository](../../README.md#running-the-examples).
