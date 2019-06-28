# A demonstration custom widget plugin for Qt Designer.
# 
# Copyright (c) 2013 Riverbank Computing Limited


from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from pydemo import PyDemo


# This class implements the interface expected by Qt Designer to access the
# custom widget.  See the description of the QDesignerCustomWidgetInterface
# class for full details.
class PyDemoPlugin(QPyDesignerCustomWidgetPlugin):

    # Initialise the instance.
    def __init__(self, parent=None):
        super(PyDemoPlugin, self).__init__(parent)

        self._initialized = False

    # Initialise the custom widget for use with the specified formEditor
    # interface.
    def initialize(self, formEditor):
        if self._initialized:
            return

        self._initialized = True

    # Return True if the custom widget has been intialised.
    def isInitialized(self):
        return self._initialized

    # Return a new instance of the custom widget with the given parent.
    def createWidget(self, parent):
        return PyDemo(parent)

    # Return the name of the class that implements the custom widget.
    def name(self):
        return "PyDemo"

    # Return the name of the group to which the custom widget belongs.  A new
    # group will be created if it doesn't already exist.
    def group(self):
        return "PyQt Examples"

    # Return the icon used to represent the custom widget in Designer's widget
    # box.
    def icon(self):
        return QIcon(_logo_pixmap)

    # Return a short description of the custom widget used by Designer in a
    # tool tip.
    def toolTip(self):
        return "PyQt demonstration widget"

    # Return a full description of the custom widget used by Designer in
    # "What's This?" help for the widget.
    def whatsThis(self):
        return "PyDemo is a demonstration custom widget written in Python " \
               "using PyQt."

    # Return True if the custom widget acts as a container for other widgets.
    def isContainer(self):
        return False

    # Return an XML fragment that allows the default values of the custom
    # widget's properties to be overridden.
    def domXml(self):
        return '<widget class="PyDemo" name="pyDemo">\n' \
               ' <property name="toolTip" >\n' \
               '  <string>PyQt demonstration widget</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis" >\n' \
               '  <string>PyDemo is a demonstration custom widget written ' \
               'in Python using PyQt.</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Return the name of the module containing the class that implements the
    # custom widget.  It may include a module path.
    def includeFile(self):
        return "pydemo"


# Define the image used for the icon.
_logo_16x16_xpm = [
"16 16 61 1",
"6 c #5bbd7c",
"a c #7aaada",
"h c #7eaddb",
"n c #7faddb",
"E c #82afdc",
"x c #83b0dd",
"C c #84b0dd",
"z c #84b1dd",
"B c #85b1dd",
"u c #87b2de",
"U c #9ec1e4",
"Z c #9fc1e4",
"H c #a1c3e5",
"Y c #a5c5e4",
"V c #a6c6e4",
"P c #afcbe2",
"S c #afcbe3",
"O c #b1cde9",
"T c #b2cee9",
"t c #b4cee3",
"r c #b5cee3",
"q c #c2d8ee",
"0 c #c7dbef",
"f c #cedddb",
"b c #cfdddb",
"1 c #d0e1f2",
"J c #d8e2d2",
"I c #d9e2d2",
"# c #dfeaf6",
"g c #e3edf7",
"K c #ecf2f9",
"N c #ecf3f9",
"o c #eeecbb",
"i c #f2edb2",
"l c #f2edb3",
"w c #f6eea6",
"v c #f7eea6",
"W c #fcee8c",
"m c #fcfdfe",
"L c #fdec73",
"k c #fedd00",
"e c #fede06",
"p c #fede07",
"j c #fee013",
"X c #fee015",
"s c #fee223",
"d c #fee32c",
"A c #fee749",
"Q c #fee850",
"R c #fee851",
"D c #fee854",
"y c #feea65",
"M c #feec74",
"c c #feed7c",
"F c #feee85",
"G c #feee86",
"5 c #fef095",
"4 c #fef195",
"3 c #fef6bb",
"2 c #fefdf5",
". c #fefefe",
"..#abcdeedcfa#..",
".ghijkkkkkkjlhg.",
"mnopkkkkkkkkponm",
"qrskkkkkkkkkkstq",
"uvkkkkkkkkkkkkwu",
"xykkkkkkkkkkkkyx",
"zAkkkkkkkkkkkkAB",
"CDkkkkkkkkkkkkDC",
"EFkkkkkkkkkkkkGE",
"HIekkkkkkkkkkeJH",
"KBLkkkkkkkkkkMBN",
".OPQkkkkkkkkRST.",
"..UVWXkkkkXWYZ..",
"...0123453210...",
"6666666666666666",
"BBBBBBBBBBBBBBBB"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
