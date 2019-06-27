from PyQt5.QtCore import QObject, pyqtSignal

class CurrentThread(QObject):

    _on_execute = pyqtSignal(object, tuple, dict)

    def __init__(self):
        super(QObject, self).__init__()
        self._on_execute.connect(self._execute_in_thread)

    def execute(self, f, args, kwargs):
        self._on_execute.emit(f, args, kwargs)

    def _execute_in_thread(self, f, args, kwargs):
        f(*args, **kwargs)

main_thread = CurrentThread()

def run_in_main_thread(f):
    def result(*args, **kwargs):
        main_thread.execute(f, args, kwargs)
    return result