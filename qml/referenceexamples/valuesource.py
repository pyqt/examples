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

from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, Q_CLASSINFO,
        QCoreApplication, QDate, QObject, QTime, QTimer, QUrl)
from PyQt5.QtGui import QColor
from PyQt5.QtQml import (qmlAttachedPropertiesObject, qmlRegisterType,
        QQmlComponent, QQmlEngine, QQmlListProperty, QQmlProperty,
        QQmlPropertyValueSource)


QML = b'''
import People 1.0
import QtQuick 2.0

BirthdayParty {
    HappyBirthdaySong on announcement { name: "Bob Jones" }

    onPartyStarted: console.log("This party started rockin' at " + time);

    host: Boy {
        name: "Bob Jones"
        shoe { size: 12; color: "white"; brand: "Nike"; price: 90.0 }
    }

    Boy {
        name: "Leo Hodges"
        BirthdayParty.rsvp: "2009-07-06"
        shoe { size: 10; color: "black"; brand: "Reebok"; price: 59.95 }
    }

    Boy {
        name: "Jack Smith"
        shoe { size: 8; color: "blue"; brand: "Puma"; price: 19.95 }
    }

    Girl {
        name: "Anne Brown"
        BirthdayParty.rsvp: "2009-07-01"
        shoe.size: 7
        shoe.color: "red"
        shoe.brand: "Marc Jacobs"
        shoe.price: 699.99
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

    shoeChanged = pyqtSignal()

    @pyqtProperty(int, notify=shoeChanged)
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if self._size != size:
            self._size = size
            self.shoeChanged.emit()

    @pyqtProperty(QColor, notify=shoeChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if self._color != color:
            self._color = color
            self.shoeChanged.emit()

    @pyqtProperty(str, notify=shoeChanged)
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, brand):
        if self._brand != brand:
            self._brand = brand
            self.shoeChanged.emit()

    @pyqtProperty(float, notify=shoeChanged)
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if self._price != price:
            self._price = price
            self.shoeChanged.emit()


class Person(QObject):
    def __init__(self, parent=None):
        super(Person, self).__init__(parent)

        self._name = ''
        self._shoe = ShoeDescription()

    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit()

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

    rsvpChanged = pyqtSignal()

    @pyqtProperty(QDate, notify=rsvpChanged)
    def rsvp(self):
        return self._rsvp

    @rsvp.setter
    def rsvp(self, rsvp):
        if self._rsvp != rsvp:
            self._rsvp = rsvp
            self.rsvpChanged.emit()


class BirthdayParty(QObject):
    Q_CLASSINFO('DefaultProperty', 'guests')

    partyStarted = pyqtSignal(QTime, arguments=['time'])

    def __init__(self, parent=None):
        super(BirthdayParty, self).__init__(parent)

        self._host = None
        self._guests = []

    hostChanged = pyqtSignal()

    @pyqtProperty(Person, notify=hostChanged)
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        if self._host != host:
            self._host = host
            self.hostChanged.emit()

    @pyqtProperty(QQmlListProperty)
    def guests(self):
        return QQmlListProperty(Person, self, self._guests)

    @pyqtProperty(str)
    def announcement(self):
        return ''

    @announcement.setter
    def announcement(self, announcement):
        print(announcement)

    def startParty(self):
        self.partyStarted.emit(QTime.currentTime())


class HappyBirthdaySong(QObject, QQmlPropertyValueSource):
    def __init__(self, parent=None):
        super(HappyBirthdaySong, self).__init__(parent)

        self._line = -1
        self._lyrics = []
        self._target = QQmlProperty()
        self._name = ''

        timer = QTimer(self)
        timer.timeout.connect(self.advance)
        timer.start(1000)

    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name

            self._lyrics = [
                "",
                "Happy birthday to you,",
                "Happy birthday to you,",
                "Happy birthday dear %s," % self._name,
                "Happy birthday to you!"
            ]

            self.nameChanged.emit()

    def setTarget(self, target):
        self._target = target

    @pyqtSlot()
    def advance(self):
        self._line += 1

        if self._line < len(self._lyrics):
            self._target.write(self._lyrics[self._line])
        else:
            QCoreApplication.instance().quit()


app = QCoreApplication(sys.argv)

qmlRegisterType(BirthdayPartyAttached)
qmlRegisterType(BirthdayParty, "People", 1, 0, "BirthdayParty",
        attachedProperties=BirthdayPartyAttached)
qmlRegisterType(HappyBirthdaySong, "People", 1, 0, "HappyBirthdaySong")
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

    party.startParty()
else:
    for e in component.errors():
        print("Error:", e.toString());

sys.exit(app.exec_())
