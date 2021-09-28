import logging

from yuzu.logging import get_annotation, setup_logging
from yuzu.cache import cache

setup_logging()
LOGGER = logging.getLogger(__file__)

log = get_annotation(LOGGER)


@log()
@cache()
def fib(x):
    if x <= 1:
        return 1
    return fib(x - 1) + fib(x - 2)


n = 10
print(f"fib({n})={fib(n)}")
