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


import sys
import random

from PyQt5.QtCore import QCoreApplication, QMutex, QThread, QWaitCondition


DataSize = 100000
BufferSize = 8192
buffer = list(range(BufferSize))

bufferNotEmpty = QWaitCondition()
bufferNotFull = QWaitCondition()
mutex = QMutex()
numUsedBytes = 0


class Producer(QThread):
    def run(self):
        global numUsedBytes

        for i in range(DataSize):
            mutex.lock()
            if numUsedBytes == BufferSize:
                bufferNotFull.wait(mutex)
            mutex.unlock()
            
            buffer[i % BufferSize] = "ACGT"[random.randint(0, 3)]

            mutex.lock()
            numUsedBytes += 1
            bufferNotEmpty.wakeAll()
            mutex.unlock()


class Consumer(QThread):
    def run(self):
        global numUsedBytes

        for i in range(DataSize):
            mutex.lock()
            if numUsedBytes == 0:
                bufferNotEmpty.wait(mutex)
            mutex.unlock()
            
            sys.stderr.write(buffer[i % BufferSize])

            mutex.lock()
            numUsedBytes -= 1
            bufferNotFull.wakeAll()
            mutex.unlock()
            
        sys.stderr.write("\n")


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()
    producer.wait()
    consumer.wait()
