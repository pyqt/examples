#============================================================================#
# PyQt5 port of the designer/containerextension example from Qt v4.x         #
#----------------------------------------------------------------------------#
import sip
from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import (QDesignerFormWindowInterface, QExtensionFactory,
        QPyDesignerContainerExtension, QPyDesignerCustomWidgetPlugin,
        QPyDesignerPropertySheetExtension)

from multipagewidget import PyMultiPageWidget


Q_TYPEID = {
    'QDesignerContainerExtension':     'org.qt-project.Qt.Designer.Container',
    'QDesignerPropertySheetExtension': 'org.qt-project.Qt.Designer.PropertySheet'
}


#============================================================================#
# ContainerExtension                                                         #
#----------------------------------------------------------------------------#
class MultiPageWidgetContainerExtension(QPyDesignerContainerExtension):
    def __init__(self, widget, parent=None):
        super(MultiPageWidgetContainerExtension, self).__init__(parent)

        self._widget = widget
            
    def addWidget(self, widget):
        self._widget.addPage(widget)
    
    def count(self):
        return self._widget.count()
    
    def currentIndex(self):
        return self._widget.getCurrentIndex()
    
    def insertWidget(self, index, widget):
        self._widget.insertPage(index, widget)
    
    def remove(self, index):
        self._widget.removePage(index)
    
    def setCurrentIndex(self, index):
        self._widget.setCurrentIndex(index)
    
    def widget(self, index):
        return self._widget.widget(index)
    

#============================================================================#
# ExtensionFactory                                                           #
#----------------------------------------------------------------------------#
class MultiPageWidgetExtensionFactory(QExtensionFactory):
    def __init__(self, parent=None):
        super(MultiPageWidgetExtensionFactory, self).__init__(parent)

    def createExtension(self, obj, iid, parent):
        if iid != Q_TYPEID['QDesignerContainerExtension']:
            return None
        if isinstance(obj, PyMultiPageWidget):
            return MultiPageWidgetContainerExtension(obj, parent)
        return None


#============================================================================#
# CustomWidgetPlugin                                                         #
#----------------------------------------------------------------------------#
class MultiPageWidgetPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):    
        super(MultiPageWidgetPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        manager = formEditor.extensionManager()
        if manager:
            self.factory = MultiPageWidgetExtensionFactory(manager)
            manager.registerExtensions(self.factory, Q_TYPEID['QDesignerContainerExtension'])
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        widget = PyMultiPageWidget(parent)
        widget.currentIndexChanged.connect(self.currentIndexChanged)
        widget.pageTitleChanged.connect(self.pageTitleChanged)
        return widget

    def name(self):
        return "PyMultiPageWidget"

    def group(self):
        return "PyQt Examples"

    def icon(self):
        return QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return True

    def domXml(self):
        return ('<widget class="PyMultiPageWidget" name="multipagewidget">'
                '  <widget class="QWidget" name="page" />'
                '</widget>')

    def includeFile(self):
        return "multipagewidget"

    def currentIndexChanged(self, index):
        widget = self.sender()
        if widget and isinstance(widget, PyMultiPageWidget):
            form = QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                form.emitSelectionChanged()

    def pageTitleChanged(self, title):
        widget = self.sender()
        if widget and isinstance(widget, PyMultiPageWidget):
            page = widget.widget(widget.getCurrentIndex())
            form = QDesignerFormWindowInterface.findFormWindow(widget)
            if form:
                editor = form.core()
                manager = editor.extensionManager()
                sheet = manager.extension(page, Q_TYPEID['QDesignerPropertySheetExtension'])
                # This explicit cast is necessary here
                sheet = sip.cast(sheet, QPyDesignerPropertySheetExtension)
                propertyIndex = sheet.indexOf('windowTitle')
                sheet.setChanged(propertyIndex, True)

#============================================================================#
# EOF                                                                        #
#----------------------------------------------------------------------------#
