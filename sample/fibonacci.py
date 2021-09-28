import logging
import sys

from yuzu.logging import get_annotation
from yuzu.cache import cache


logging.\
    getLogger().\
    addHandler(
        logging.StreamHandler(sys.stderr)
    )


LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.DEBUG)

log = get_annotation(LOGGER)


@log()
@cache()
def fib(x):
    if x <= 1:
        return 1
    return fib(x - 1) + fib(x - 2)


n = 10
print(f"fib({n})={fib(n)}")
