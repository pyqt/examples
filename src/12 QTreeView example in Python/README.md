# QTreeView example in Python

A _tree view_ is what's classicaly used to display files and folders: A hierarchical structure where items can be expanded. This example application shows how PyQt5's [`QTreeView`](https://doc.qt.io/qt-5/qtreeview.html) can be used to display your local files.

<p align="center"><img src="../screenshots/qtreeview-example-in-python.png" alt="QTreeView example in Python"></p>

As for the other examples in this repository, the code lies in [`main.py`](main.py). The important steps are:

    model = QDirModel()
    view = QTreeView()
    view.setModel(model)
    view.setRootIndex(model.index(home_directory))
    view.show()

Both [`QDirModel`](https://doc.qt.io/qt-5/qdirmodel.html) and [`QTreeView`](https://doc.qt.io/qt-5/qtreeview.html) are a part of Qt's [Model/View framework](https://doc.qt.io/qt-5/model-view-programming.html). The idea is that the model provides data to the view, which then displays it. As you can see above, we first instantiate the model and the view, then connect the two via `.setModel(...)`. The `.setRootIndex(...)` call instructs the view to display the files in your home directory.

The nice thing about the Model/View distinction is that it lets you visualize the same data in different ways. For instance, you could replace the line `view = QTreeView()` above by the following to display a flat _list_ of your files instead:

    view = QListView()

The next example, [PyQt5 QListview](../13%20PyQt5%20QListView), shows another way of using `QListView`.

To run this example yourself, please follow [the instructions in the README of this repository](../../README.md#running-the-examples).
