import logging
import os
import re
import sys
from functools import wraps

LOGGERS = []


def setup_logger(logfile=None, debug=False):
    for l in LOGGERS:
        setup_logger1(l, logfile, debug)


def get_logger(name):
    ret = logging.getLogger(name)
    LOGGERS.append(ret)
    return ret


def setup_logger1(LOGGER, logfile, debug=False):
    if not logfile:
        logfile = os.path.join(os.getcwd(), "yuzu.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    to_stderr = logging.StreamHandler(sys.stderr)
    to_stderr.setFormatter(formatter)
    to_file = logging.FileHandler(logfile)
    to_file.setFormatter(formatter)
    LOGGER.addHandler(to_stderr)
    LOGGER.addHandler(to_file)
    if not debug:
        LOGGER.setLevel(logging.INFO)
        to_stderr.setLevel(logging.INFO)
        to_file.setLevel(logging.INFO)
    else:
        LOGGER.setLevel(logging.DEBUG)
        to_stderr.setLevel(logging.DEBUG)
        to_file.setLevel(logging.DEBUG)


def get_annotation(LOGGER):
    def log(ignore_args=[], ignore_kw=[], return_value=True):
        def annotator(f):
            @wraps(f)
            def executor(*args, **kw):
                args_ = [a for i, a in enumerate(args) if i not in ignore_args]
                kw_ = {k: v for k, v in kw.items() if k not in ignore_kw}
                LOGGER.info(f"{f.__name__} {args_} {kw_} start")
                ret = f(*args, **kw)
                if return_value:
                    LOGGER.info(f"{f.__name__} end, value={ret}")
                else:
                    LOGGER.info(f"{f.__name__} end")
                return ret

            return executor

        return annotator

    return log
