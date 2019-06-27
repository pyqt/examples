"""
A more powerful, synchronous implementation of run_in_main_thread(...).
It allows you to receive results from the function invocation:

    @run_in_main_thread
    def return_2():
        return 2
    
    # Runs the above function in the main thread and prints '2':
    print(return_2())
"""

from functools import wraps
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication
from threading import Event, get_ident

def run_in_thread(thread_fn):
    def decorator(f):
        @wraps(f)
        def result(*args, **kwargs):
            thread = thread_fn()
            return Executor.instance().run_in_thread(thread, f, args, kwargs)
        return result
    return decorator

def _main_thread():
    app = QApplication.instance()
    if app:
        return app.thread()
    # We reach here in tests that don't (want to) create a QApplication.
    if int(QThread.currentThreadId()) == get_ident():
        return QThread.currentThread()
    raise RuntimeError('Could not determine main thread')

run_in_main_thread = run_in_thread(_main_thread)

def is_in_main_thread():
    return QThread.currentThread() == _main_thread()

class Executor:

    _INSTANCE = None

    @classmethod
    def instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(QApplication.instance())
        return cls._INSTANCE
    def __init__(self, app):
        self._pending_tasks = []
        self._app_is_about_to_quit = False
        app.aboutToQuit.connect(self._about_to_quit)
    def _about_to_quit(self):
        self._app_is_about_to_quit = True
        for task in self._pending_tasks:
            task.set_exception(SystemExit())
            task.has_run.set()
    def run_in_thread(self, thread, f, args, kwargs):
        if QThread.currentThread() == thread:
            return f(*args, **kwargs)
        elif self._app_is_about_to_quit:
            # In this case, the target thread's event loop most likely is not
            # running any more. This would mean that our task (which is
            # submitted to the event loop via signals/slots) is never run.
            raise SystemExit()
        task = Task(f, args, kwargs)
        self._pending_tasks.append(task)
        try:
            receiver = Receiver(task)
            receiver.moveToThread(thread)
            sender = Sender()
            sender.signal.connect(receiver.slot)
            sender.signal.emit()
            task.has_run.wait()
            return task.result
        finally:
            self._pending_tasks.remove(task)

class Task:
    def __init__(self, fn, args, kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.has_run = Event()
        self._result = self._exception = None
    def __call__(self):
        try:
            self._result = self._fn(*self._args, **self._kwargs)
        except Exception as e:
            self._exception = e
        finally:
            self.has_run.set()
    def set_exception(self, exception):
        self._exception = exception
    @property
    def result(self):
        if not self.has_run.is_set():
            raise ValueError("Hasn't run.")
        if self._exception:
            raise self._exception
        return self._result

class Sender(QObject):
    signal = pyqtSignal()

class Receiver(QObject):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
    def slot(self):
        self.callback()