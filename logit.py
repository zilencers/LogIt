import sys, traceback
from enum import Enum
from datetime import datetime
from functools import wraps


class LogIt():
    def __init__(self):
        self._filename = None
        self._level = None
        self._format = None
        self._dt_format = None
        self._func_name = None
        self._func_module = None
        self._func_args = None

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

    def _write(self, log_level, message):
        dt = datetime.now().strftime(self._dt_format)
        print(dt)
    
    def _check_config(self):
        if self._filename is not None:
            return True
        return False

    def _console(self, message):
        print(message)

    def debug(self, message):
        self._write(Level.Debug, message)

    def info(self, message):
        if self._check_config():
            self._write(Level.Info, message)
        else:
            self._console(message)

    def warning(self, message):
        if self._check_config():
            self._write(Level.Warn, message)
        else:
            self._console(message)

    def error(self, message):
        if self._check_config():
            self._write(Level.Error, message)
        else:
            self._console(message)

    def fatal(self, message):
        if self._check_config():
            self._write(Level.Fatal, message)
        else:
            self._console(message)

    def exception(self, message):
        if self._check_config():
            self._write(Level.Fatal, message)
        else:
            self._console(message)

        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=self._filename)

class Level(Enum):
    Debug = 0,
    Info = 1,
    Warn = 2,
    Error = 3,
    Fatal = 4