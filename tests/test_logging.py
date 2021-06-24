from yuzu import logging

import pytest


def test_logging():
    LOGGER = logging.get_logger(__file__)
    log = logging.get_annotation(LOGGER)
    logging.setup_logger(__file__)

    @log(log_args=[0])
    def func(x):
        return x

    func(1)
