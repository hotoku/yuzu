from tempfile import TemporaryDirectory
from pathlib import Path
import os

from yuzu import logging


def test_logging():
    """
    It logs arguments and a return value.
    """
    with TemporaryDirectory() as d:
        logfile = Path(d) / "test.log"
        LOGGER = logging.get_logger(__file__)
        log = logging.get_annotation(LOGGER)
        logging.setup_logger(logfile.as_posix())

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
    It logs to `yuzu.log` as defaut.
    """
    with TemporaryDirectory() as d, ChangeDirectory(d):
        LOGGER = logging.get_logger(__file__)
        log = logging.get_annotation(LOGGER)
        logging.setup_logger()

        @log()
        def func(x, y=2):
            return x + y

        func(1)
        func(3, y=4)

        with open("./yuzu.log") as f:
            logs = "\n".join(f.readlines())

        assert "func [1] {}" in logs
        assert "value=3" in logs
        assert "func [3] {'y': 4}" in logs
        assert "value=7" in logs
