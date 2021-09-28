from tempfile import TemporaryDirectory
from pathlib import Path
import os
import logging
import sys

from yuzu import logging as yl


def setup_logger(LOGGER, logfile=None, debug=False):
    if logfile is None:
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


def test_logging():
    """
    It logs arguments and a return value.
    """
    with TemporaryDirectory() as d:
        logfile = Path(d) / "test.log"
        LOGGER = logging.getLogger(__file__ + "__test_logging")
        log = yl.get_annotation(LOGGER)
        setup_logger(LOGGER, logfile.as_posix())

        @log()
        def func(x, y=2):
            return x + y

        func(1)
        func(3, y=4)

        with open(logfile) as f:
            logs = "\n".join(f.readlines())

        assert "func [1] {}" in logs
        assert "value=3" in logs
        assert "func [3] {'y': 4}" in logs
        assert "value=7" in logs


class ChangeDirectory:
    def __init__(self, d) -> None:
        self.curdir = os.getcwd()
        self.targetdir = d

    def __enter__(self):
        os.chdir(self.targetdir)

    def __exit__(self, *args):
        os.chdir(self.curdir)


def test_ignore():
    """
    It does not log arguments if ignore_args is given.
    """
    with TemporaryDirectory() as d, ChangeDirectory(d):
        LOGGER = logging.getLogger(__file__ + "__test_ignore")
        log = yl.get_annotation(LOGGER)
        setup_logger(LOGGER)

        @log(ignore_args=[0])
        def func(x, y=2):
            return x + y

        func(1)
        func(3, y=4)

        with open("./yuzu.log") as f:
            logs = "\n".join(f.readlines())

        assert "func [1] {}" not in logs
        assert "func [] {}" in logs
        assert "value=3" in logs
        assert "func [] {'y': 4}" in logs
        assert "value=7" in logs


def test_ignore_kw():
    """
    It does not log arguments if ignore_kw is given.
    """
    with TemporaryDirectory() as d, ChangeDirectory(d):
        LOGGER = logging.getLogger(__file__ + "__test_ignore_kw")
        log = yl.get_annotation(LOGGER)
        setup_logger(LOGGER)

        @log(ignore_kw=["y"])
        def func(x, y=2):
            return x + y

        func(1)
        func(3, y=4)

        with open("./yuzu.log") as f:
            logs = "\n".join(f.readlines())

        assert "func [1] {}" in logs
        assert "value=3" in logs
        assert "func [3] {}" in logs
        assert "value=7" in logs


def test_ignore_return():
    """
    It does not log the return value if return_value=False.
    """
    with TemporaryDirectory() as d, ChangeDirectory(d):
        LOGGER = logging.getLogger(__file__ + "__test_ignore_return")
        log = yl.get_annotation(LOGGER)
        setup_logger(LOGGER)

        @log(return_value=False)
        def func(x, y=2):
            return x + y

        func(1)
        func(3, y=4)

        with open("./yuzu.log") as f:
            logs = "\n".join(f.readlines())

        assert "func [1] {}" in logs
        assert "value=3" not in logs
        assert "func [3] {'y': 4}" in logs
        assert "value=7" not in logs
