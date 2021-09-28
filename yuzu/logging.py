import logging
import os
from functools import wraps
import sys
from typing import Callable, List, Optional


def setup_logging(level: int = logging.INFO,
                  logfile: Optional[str] = None,
                  format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s") -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter(format_str)

    to_stderr = logging.StreamHandler(sys.stderr)
    root_logger.addHandler(to_stderr)
    to_stderr.setFormatter(formatter)
    if logfile is not None:
        to_file = logging.FileHandler(logfile)
        root_logger.addHandler(to_file)
        to_file.setFormatter(formatter)


def get_annotation(LOGGER: logging.Logger):
    def log(ignore_args: List[int] = [], ignore_kw: List[str] = [], return_value=True):
        def annotator(f: Callable):
            @wraps(f)
            def executor(*args, **kw):
                args_ = [a for i, a in enumerate(args) if i not in ignore_args]
                kw_ = {k: v for k, v in kw.items() if k not in ignore_kw}
                LOGGER.info(
                    f"{f.__name__} {args_} {kw_} start (pid={os.getpid()})")
                ret = f(*args, **kw)
                if return_value:
                    LOGGER.info(
                        f"{f.__name__} end (pid={os.getpid()}), value={ret}")
                else:
                    LOGGER.info(f"{f.__name__} end (pid={os.getpid()})")
                return ret
            return executor
        return annotator
    return log
