#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
        QSqlRelationalTableModel, QSqlTableModel)

import connection


def initializeModel(model):
    model.setTable('employee')

    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model.setRelation(2, QSqlRelation('city', 'id', 'name'))
    model.setRelation(3, QSqlRelation('country', 'id', 'name'))

    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "Name")
    model.setHeaderData(2, Qt.Horizontal, "City")
    model.setHeaderData(3, Qt.Horizontal, "Country")

    model.select()


def createView(title, model):
    view = QTableView()
    view.setModel(model)
    view.setItemDelegate(QSqlRelationalDelegate(view))
    view.setWindowTitle(title)

    return view


def createRelationalTables():
    query = QSqlQuery()

    query.exec_("create table employee(id int, name varchar(20), city int, country int)")
    query.exec_("insert into employee values(1, 'Espen', 5000, 47)")
    query.exec_("insert into employee values(2, 'Harald', 80000, 49)")
    query.exec_("insert into employee values(3, 'Sam', 100, 41)")

    query.exec_("create table city(id int, name varchar(20))")
    query.exec_("insert into city values(100, 'San Jose')")
    query.exec_("insert into city values(5000, 'Oslo')")
    query.exec_("insert into city values(80000, 'Munich')")

    query.exec_("create table country(id int, name varchar(20))")
    query.exec_("insert into country values(41, 'USA')")
    query.exec_("insert into country values(47, 'Norway')")
    query.exec_("insert into country values(49, 'Germany')")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    createRelationalTables()

    model = QSqlRelationalTableModel()

    initializeModel(model)

    view = createView("Relational Table Model", model)

    view.show()

    sys.exit(app.exec_())
