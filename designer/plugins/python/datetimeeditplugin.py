#============================================================================#
# Designer plugins for PyDateEdit and PyDateTimeEdit                         #
#----------------------------------------------------------------------------#
# Copyright (c) 2008 by Denviso GmbH, <ulrich.berning@denviso.de>            #
#                                                                            #
# All Rights Reserved                                                        #
#                                                                            #
# Permission to use, copy, modify, and distribute this software and its      #
# documentation for any purpose and without fee is hereby granted,           #
# provided that the above copyright notice appear in all copies and that     #
# both that copyright notice and this permission notice appear in            #
# supporting documentation.                                                  #
#                                                                            #
# DENVISO DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS                       #
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY              #
# AND FITNESS, IN NO EVENT SHALL DENVISO BE LIABLE FOR ANY                   #
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES                  #
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,                    #
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER                      #
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE              #
# OR PERFORMANCE OF THIS SOFTWARE.                                           #
#----------------------------------------------------------------------------#


from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from datetimeedit import PyDateEdit, PyDateTimeEdit


#============================================================================#
# The group name in designer widgetbox                                       #
#----------------------------------------------------------------------------#
DESIGNER_GROUP_NAME = "PyQt Examples"


#============================================================================#
# Plugin for PyDateEdit                                                      #
#----------------------------------------------------------------------------#
class PyDateEditPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(PyDateEditPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def isContainer(self):
        return False

    def icon(self):
        return QIcon()

    def domXml(self):
        return '<widget class="PyDateEdit" name="pyDateEdit">\n</widget>\n'
    
    def group(self):
        return DESIGNER_GROUP_NAME
              
    def includeFile(self):
        return "datetimeedit"

    def name(self):
        return "PyDateEdit"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def createWidget(self, parent):
        return PyDateEdit(parent)


#============================================================================#
# Plugin for PyDateTimeEdit                                                  #
#----------------------------------------------------------------------------#
class PyDateTimeEditPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(PyDateTimeEditPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def isContainer(self):
        return False

    def icon(self):
        return QIcon()

    def domXml(self):
        return '<widget class="PyDateTimeEdit" name="pyDateTimeEdit">\n</widget>\n'
    
    def group(self):
        return DESIGNER_GROUP_NAME
              
    def includeFile(self):
        return "datetimeedit"

    def name(self):
        return "PyDateTimeEdit"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def createWidget(self, parent):
        return PyDateTimeEdit(parent)
