import pytest


from yuzu import cache, activate_cache, deactivate_cache, clear_cache


@pytest.fixture
def clear():
    clear_cache()


def test_cache1(clear):
    """
    When the function is called twice with same argument,
    the function is not executed in the second time.
    The returned values are same.
    """
    num = 0

    @cache()
    def func(x):
        nonlocal num
        num += 1
        return x + 1
    assert num == 0
    ret1 = func(1)
    assert num == 1
    ret1_ = func(1)
    assert num == 1
    assert ret1 == ret1_
    ret2 = func(2)
    assert num == 2
    assert not ret1 == ret2


def test_cache2(clear):
    """
    The arguments in `ignore_args` are not considered for cache evaluation.
    """
    num = 0

    @cache(ignore_args=[0, 2])
    def func(x, y, z):
        nonlocal num
        num += 1
        return y + 1

    assert num == 0
    ret1 = func(0, 1, 2)
    assert num == 1
    ret1_ = func(1, 1, 3)
    assert num == 1
    assert ret1 == ret1_

    ret2 = func(3, 4, 5)
    assert num == 2
    assert ret2 != ret1


def test_cache3(clear):
    """
    The arguments in `ignore_kw` are not considered for cache evaluation.
    """
    num = 0

    @cache(ignore_kw=["x", "z"])
    def func(x=0, y=0, z=0):
        nonlocal num
        num += 1
        return y + 1

    assert num == 0
    ret1 = func(x=0, y=1, z=2)
    assert num == 1
    ret1_ = func(x=1, y=1, z=3)
    assert num == 1
    assert ret1 == ret1_

    ret2 = func(x=3, y=4, z=5)
    assert num == 2
    assert ret2 != ret1


def test_cache4(clear):
    """
    Calling `activate_cache` switches cache usage.
    """
    num = 0

    @cache()
    def func(x):
        nonlocal num
        num += 1
        return x + 1
    assert num == 0
    func(1)
    assert num == 1
    func(1)
    assert num == 1
    deactivate_cache()
    func(1)
    assert num == 2
    activate_cache()
    func(1)
    assert num == 2


def test_cache5(clear):
    """
    Check keyword arguments
    """
    num = 0

    @cache()
    def func(x, y):
        nonlocal num
        num += 1
        return x + y
    assert num == 0
    func(x=1, y=2)
    assert num == 1
    func(y=2, x=1)
    assert num == 1
