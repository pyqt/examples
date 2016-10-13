#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain additional
## rights.  These rights are described in the Nokia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you have questions regarding the use of this file, please contact
## Nokia at qt-info@nokia.com.
## $QT_END_LICENSE$
##
#############################################################################


from colors import Colors


class Score(object):
    LOCK_ITEMS, UNLOCK_ITEMS, SKIP_LOCK = range(3)

    FROM_CURRENT, FROM_START, NEW_ANIMATION_ONLY, ONLY_IF_VISIBLE = range(4)

    def __init__(self):
        self._index = {}
        self._playlist = []

    def hasQueuedMovies(self):
        return len(self._playlist) > 0

    def prepare(self, movie, runMode, lockMode):
        if lockMode == Score.LOCK_ITEMS:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.isVisible():
                    item.setEnabled(False)
                    item.prepare()
        elif lockMode == Score.UNLOCK_ITEMS:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.isVisible():
                    item.setEnabled(True)
                    item.prepare()
        else:
            for item in movie:
                if runMode != Score.ONLY_IF_VISIBLE or item.isVisible():
                    item.prepare()

    def _play(self, movie, runMode):
        if runMode == Score.NEW_ANIMATION_ONLY:
            for item in movie:
                if item.notOwnerOfItem():
                    item.play(True)
        elif runMode == Score.ONLY_IF_VISIBLE:
            for item in movie:
                if item.isVisible():
                    item.play(runMode == Score.FROM_START)
        else:
            for item in movie:
                item.play(runMode == Score.FROM_START)

    def queueMovie(self, indexName, runMode=FROM_START, lockMode=SKIP_LOCK):
        try:
            movie = self._index[indexName]
        except KeyError:
            Colors.debug("Queuing movie:", indexName, "(does not exist)")
            return

        self.prepare(movie, runMode, lockMode)
        self._playlist.append((movie, runMode))
        Colors.debug("Queuing movie:", indexName)

    def playQue(self):
        for movie, runMode in self._playlist:
            self._play(movie, runMode)

        self._playlist = []
        Colors.debug("********* Playing que *********")

    def insertMovie(self, indexName):
        movie = []
        self._index[indexName] = movie

        return movie
