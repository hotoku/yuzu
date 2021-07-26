from tempfile import TemporaryDirectory
from pathlib import Path

from yuzu import logging


def test_logging():
    with TemporaryDirectory() as d:
        logfile = Path(d) / "test.log"
        LOGGER = logging.get_logger(__file__)
        log = logging.get_annotation(LOGGER)
        logging.setup_logger(logfile.as_posix())

        @log()
        def func(x):
            return x

        func(1)

        with open(logfile) as f:
            logs = "\n".join(f.readlines())
        assert "func [1]" in logs
        assert "value=1" in logs
