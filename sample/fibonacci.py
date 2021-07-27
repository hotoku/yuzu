from sys import argv
from yuzu.cache import cache
from yuzu.logging import get_logger, get_annotation, setup_logger

LOGGER = get_logger(__file__)
log = get_annotation(LOGGER)
setup_logger()


@log()
@cache()
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)


n = int(argv[1])
print(f"fib({n})={fib(n)}")
