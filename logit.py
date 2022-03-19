# LOG DIRECTIVES
  # %L = Log Level
  # %N = Module
  # %F = Function
  # %P = Parameters
  # %O = Output string

from datetime import datetime


class LogIt():
    def __init__(self, str_format=""):
        self._queue = None
        self._format = str_format if str_format else "%Y%m%d %H:%M:%S %L %N %F %P %O"
        self._dt_directives=['%a','%A','%b','%B','%c','%C','%d','%D','%e','%g','%G','%h', 
                       '%H','%I','%j','%m','%M','%n','%p','%r','%R', '%S','%t','%T','%u', 
                       '%U','%W','%w','%x','%X','%y','%Y','%Z','%z','%%']
        self._log_directives = ['%L','%N','%F','%P','%O']

    def _write(self, log_level, message):
        dt = datetime.now().strftime(self._get_dt_str())
        print(dt)


    def _get_dt_str(self):
        fmt_str_list = list(self._format)

        directive = {}
        for i in range(len(fmt_str_list)):
            if self._format[i:i+1] == "%":
                if self._format[i:i] != "%":
                    for d in self._dt_directives:
                        if self._format[i:i+2] == d:
                            directive.update({self._format[i:i+2]: i})

        dt_fmt = ""
        for key, val in directive.items():
            if key == "%H":
                dt_fmt += " " + key
            elif key == "%M":
                dt_fmt += ":" + key
            elif key == "%S":
                dt_fmt += ":" + key
            else:
                dt_fmt += key

        return dt_fmt


    def console():
        print("Logging to the console")


    def info(self, message):
        self._write("INFO", message)


    def warning(self, message):
        self._write("WARN", message)


    def error(self, message):
        self._write("ERROR", message)


    def fatal(self, message):
        self._write("FATAL", message)


    def debug(self, message):
        self._write("DEBUG", message)


def trace(func):
    def inner1(*args, **kwargs):
        msg = "Func: {0}  Module: {1}  Args: {2}".format(
            func.__name__,
            func.__module__,
            args)

        print(msg)

        #console_log(msg, log_level=LogLevel.Log_Level_Debug.value)

        func(*args, **kwargs)
    return inner1