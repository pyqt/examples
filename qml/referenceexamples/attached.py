#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
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


import sys

from PyQt5.QtCore import (pyqtProperty, Q_CLASSINFO, QCoreApplication, QDate,
        QObject, QUrl)
from PyQt5.QtGui import QColor
from PyQt5.QtQml import (qmlAttachedPropertiesObject, qmlRegisterType,
        QQmlComponent, QQmlEngine, QQmlListProperty)


QML = b'''
import People 1.0
import QtQuick 2.0

BirthdayParty {
    Boy {
        name: "Robert Campbell"
        BirthdayParty.rsvp: "2009-07-01"
    }

    Boy {
        name: "Leo Hodges"
        shoe { size: 10; color: "black"; brand: "Reebok"; price: 59.95 }
        BirthdayParty.rsvp: "2009-07-06"
    }

    host: Boy {
        name: "Jack Smith"
        shoe { size: 8; color: "blue"; brand: "Puma"; price: 19.95 }
    }
}
'''


class ShoeDescription(QObject):
    def __init__(self, parent=None):
        super(ShoeDescription, self).__init__(parent)

        self._size = 0
        self._color = QColor()
        self._brand = ''
        self._price = 0.0

    @pyqtProperty(int)
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @pyqtProperty(str)
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, brand):
        self._brand = brand

    @pyqtProperty(float)
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price


class Person(QObject):
    def __init__(self, parent=None):
        super(Person, self).__init__(parent)

        self._name = ''
        self._shoe = ShoeDescription()

    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @pyqtProperty(ShoeDescription)
    def shoe(self):
        return self._shoe


class Boy(Person):
    pass


class Girl(Person):
    pass


class BirthdayPartyAttached(QObject):
    def __init__(self, parent):
        super(BirthdayPartyAttached, self).__init__(parent)

        self._rsvp = QDate()

    @pyqtProperty(QDate)
    def rsvp(self):
        return self._rsvp

    @rsvp.setter
    def rsvp(self, rsvp):
        self._rsvp = rsvp


class BirthdayParty(QObject):
    Q_CLASSINFO('DefaultProperty', 'guests')

    def __init__(self, parent=None):
        super(BirthdayParty, self).__init__(parent)

        self._host = None
        self._guests = []

    @pyqtProperty(Person)
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @pyqtProperty(QQmlListProperty)
    def guests(self):
        return QQmlListProperty(Person, self, self._guests)


app = QCoreApplication(sys.argv)

qmlRegisterType(BirthdayPartyAttached)
qmlRegisterType(BirthdayParty, "People", 1, 0, "BirthdayParty",
        attachedProperties=BirthdayPartyAttached)
qmlRegisterType(ShoeDescription)
qmlRegisterType(Person)
qmlRegisterType(Boy, "People", 1, 0, "Boy")
qmlRegisterType(Girl, "People", 1, 0, "Girl")

engine = QQmlEngine()

component = QQmlComponent(engine)
component.setData(QML, QUrl())

party = component.create()

if party is not None and party.host is not None:
    print("\"%s\" is having a birthday!" % party.host.name)

    if isinstance(party.host, Boy):
        print("He is inviting:")
    else:
        print("She is inviting:")

    for guest in party.guests:
        attached = qmlAttachedPropertiesObject(BirthdayParty, guest, False)

        if attached is not None:
            rsvpDate = attached.property('rsvp')
        else:
            rsvpDate = QDate()

        if rsvpDate.isNull():
            print("    \"%s\" RSVP date: Hasn't RSVP'd" % guest.name)
        else:
            print("    \"%s\" RSVP date: %s" % (guest.name, rsvpDate.toString()))
else:
    for e in component.errors():
        print("Error:", e.toString());
