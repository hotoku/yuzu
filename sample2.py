import sys

from yuzu import logging
from yuzu.cache import cache

LOGGER = logging.get_logger(__file__)
log = logging.get_annotation(LOGGER)
logging.setup_logger()


@log()
@cache()
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)


n = int(sys.argv[1])
print(f"fib({n})={fib(n)}")
