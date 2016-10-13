#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
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

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtDBus import QDBusConnection, QDBusInterface


def method1():
    sys.stdout.write("Method 1:\n")

    reply = QDBusConnection.sessionBus().interface().registeredServiceNames()
    if not reply.isValid():
        sys.stdout.write("Error: %s\n" % reply.error().message())
        sys.exit(1)

    # Mimic the output from the C++ version.
    for name in reply.value():
        sys.stdout.write('"%s"\n' % name)


def method2():
    sys.stdout.write("Method 2:\n")

    bus = QDBusConnection.sessionBus()
    dbus_iface = QDBusInterface('org.freedesktop.DBus',
            '/org/freedesktop/DBus', 'org.freedesktop.DBus', bus)
    names = dbus_iface.call('ListNames').arguments()[0]

    # Mimic the output from the C++ version.
    sys.stdout.write('QVariant(QStringList, ("%s") )\n' % '", "'.join(names))


def method3():
    sys.stdout.write("Method 3:\n")

    names = QDBusConnection.sessionBus().interface().registeredServiceNames().value()

    # Mimic the output from the C++ version.
    sys.stdout.write('("%s")\n' % '", "'.join(names))


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)

    if not QDBusConnection.sessionBus().isConnected():
        sys.stderr.write("Cannot connect to the D-Bus session bus.\n"
                "To start it, run:\n"
                "\teval `dbus-launch --auto-syntax`\n");
        sys.exit(1)

    method1()
    method2()
    method3()

    sys.exit()
