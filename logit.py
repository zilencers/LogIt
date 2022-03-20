import sys, traceback
from threading import Thread
from enum import Enum
from datetime import datetime
from functools import wraps
from queue import Queue

class LogIt():
    def __init__(self):
        self._filename = None
        self._level = None
        self._format = None
        self._dt_format = None
        self._func_name = None
        self._func_module = None
        self._func_args = None
        self._queue = Queue()
        self._file_handler = open(self._filename, 'a')
        self._finished = False
        Thread(name="Writer", target=self._worker).start()

    def config(self, filename=None, level=None, format=None, dt_fmt=None):
        self._filename = filename
        self._level = level
        self._format = format
        self._dt_format = dt_fmt

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            self._func_name = fn.__name__
            self._func_module = fn.__module__
            self._func_args = args
            result = fn(*args, **kwargs)
            return result
        return wrapper

    def worker(self):
        # TODO: Refactor this code....
        while not self._finished:
            try:
                data = self._queue.get(True, 1)
            except Queue.Empty:
                continue

            self._file_handler.write(data)
            self._queue.task_done()

    def flush(self):
        self._queue.join()
        self._finished = True
        self._file_handler.close()

    def _write(self, log_level, message):
        dt = datetime.now().strftime(self._dt_format)
        self._queue.put(dt)
    
    def _check_config(self, level, message):
        if self._filename is not None:
            self._write(level, message)
        else:
            self._console(level, message)

    def _console(self, level, message):
        print("{0}: {1}".format(level, message))

    def debug(self, message):
        self._write(Level.Debug, message)

    def info(self, message):
        self._check_config(Level.Info, message)

    def warning(self, message):
        self._check_config(Level.Warn, message)

    def error(self, message):
        self._check_config(Level.Error, message)

    def fatal(self, message):
        self._check_config(Level.Fatal, message)

    def exception(self, message):
        self._check_config(Level.Fatal, message)

        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=self._filename)

class Level(Enum):
    Debug = 0,
    Info = 1,
    Warn = 2,
    Error = 3,
    Fatal = 4