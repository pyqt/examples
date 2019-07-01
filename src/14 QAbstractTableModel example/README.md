# QAbstractTableModel example

This [`QAbstractTableModel`](https://doc.qt.io/qt-5/qabstracttablemodel.html) example shows how you can define a custom Qt _model_ to display tabular data.

<p align="center"><img src="../screenshots/qabstracttablemodel-example.png" alt="QAbstractTableModel example"></p>

The data is a table of famous scientists. In Python, it can be written as follows:

```
headers = ["Scientist name", "Birthdate", "Contribution"]
rows =    [("Newton", "1643-01-04", "Classical mechanics"),
           ("Einstein", "1879-03-14", "Relativity"),
           ("Darwin", "1809-02-12", "Evolution")]
```

To make Qt display these data in a table, we need to answer the following questions:

 1. How many rows are there?
 2. How many columns?
 3. What's the value of each cell?
 4. What are the (column) headers?

We do this by subclassing `QAbstractTableModel`. This lets us answer each of the above questions by implementing a corresponding method:

```
class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        # How many rows are there?
        return len(rows)
    def columnCount(self, parent):
        # How many columns?
        return len(headers)
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        # What's the value of the cell at the given index?
        return rows[index.row()][index.column()]
    def headerData(self, section, orientation, role:
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        # What's the header for the given column?
        return headers[section]
```

Once we have this model, we can instantiate it, connect it to a `QTableView` and show it in a window:

    model = TableModel()
    view = QTableView()
    view.setModel(model)
    view.show()

The full code is in [`main.py`](main.py). For instructions how to run it, please see [the instructions in the README of this repository](../../README.md#running-the-examples).
