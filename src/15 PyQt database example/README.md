# PyQt database example

This example shows how you can connect to a database from a PyQt application. 

<p align="center"><img src="../screenshots/pyqt-database-example.png" alt="PyQt database example"></p>

The screenshot shows a table of project data that comes from a SQL database. One of the projects is real ;-) (Though the income is made up.)

There are many different database systems: MySQL, PostgreSQL, etc. For simplicity, this example uses SQLite because it ships with Python and doesn't require separate installation.

The default way of connecting to a database in Python is the [Database API v2.0](https://www.python.org/dev/peps/pep-0249/). You can see an example of its use in [`initdb.py`](initdb.py). Essentially, you use `.connect(...)` to connect to a database, `.cursor()` to obtain a cursor for data querying / manipulation, and `.commit()` to save any changes you made:

    import sqlite3
    connection = sqlite3.connect("projects.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE projects ...")
    cursor.execute("INSERT INTO projects ...")
    connection.commit()

The above code creates the SQLite file `projects.db` with a copy of the data shown in the screenshot.

Qt also has its own facilities for connecting to a database. You can see this in [`main.py`](main.py), where we open the `projects.db` file created above and display its data:

```
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("projects.db")
db.open()
model = QSqlTableModel(None, db)
model.setTable("projects")
model.select()
view = QTableView()
view.setModel(model)
view.show()
```

As in [previous examples](../12%20QTreeView%20example%20in%20Python), this uses Qt's Model/View framework to separate the two concerns of obtaining and displaying the data: We use `model` to load the database, and `view` to display it.

To run this example yourself, first follow [these instructions](../../README.md#running-the-examples). Then invoke `python initdb.py` to initialize the database. After that, you can execute `python main.py` to start the sample application.

While we use SQLite here, you can easily use other database systems as well. For instance, you could use PostgreSQL via the [psycopg2](http://initd.org/psycopg/) library.
