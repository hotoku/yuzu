#!/usr/bin/env python

import subprocess as sp

import click

from yuzu.cache import cache, activate_cache
from yuzu.logging import get_logger, get_annotation, setup_logger

LOGGER = get_logger(__file__)
log = get_annotation(LOGGER)

@log(log_args=[0, 1])
@cache()
def f(x, y):
    print("calculating", x, y)
    return x + y

@log()
@cache(ignore_args=[1])
def g(url, getter):
    return getter.get(url)


class Getter:
    def __init__(self):
        pass

    def get(self, url):
        ret = sp.run([
            "curl",
            url
        ],
               stdout=sp.PIPE,
               stderr=sp.PIPE)
        return {
            "stdout": ret.stdout,
            "stderr": ret.stderr
        }

class Greeter:
    def __init__(self):
        pass

    @cache(ignore_args=[0])
    def greet(self, name):
        return f"Hello {name} !"

class Greeter2:
    def __init__(self):
        pass

    @cache(ignore_args=[0])
    def greet(self, name):
        return f"Bon jour {name} !"
    

@click.command()
@click.option("--debug/--nodebug", type=bool, default=False)
@click.option("--cache/--nocache", type=bool, default=True)
def main(debug, cache):
    setup_logger("sample.log", debug)
    LOGGER.debug("debug message")

    activate_cache(cache)

    print(f(1, 1))
    print(f(2, 1))
    print(f(1, 1))
    print(g("https://google.com", Getter()))

    gr = Greeter()
    print(gr.greet("inoue"))
    print(gr.greet("inoue"))

    gr2 = Greeter2()
    print(gr.greet("inoue"))
    print(gr.greet("inoue"))
    


if __name__ == "__main__":
    main()
