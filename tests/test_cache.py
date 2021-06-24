from yuzu.cache import cache, activate_cache, clear_cache

import pytest

@pytest.fixture
def clear():
    clear_cache()


def test_cache1(clear):
    """
    同じ引数で複数回呼ばれた場合、関数は一度だけ呼び出される。
    同じ引数で呼び出した場合、返り値は同じ値。
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
    ignore_argに指定された引数は、キャッシュ判定の際に無視される。
    """
    num = 0
    @cache(ignore_args=[0,2])
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
    ignore_argに指定された引数は、キャッシュ判定の際に無視される。
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
