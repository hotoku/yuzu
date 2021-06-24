from yuzu.cache import cache, activate_cache, clear_cache

import pytest

@pytest.fixture
def clear():
    clear_cache()


def test_cache1(clear):
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
    func(2)
    assert num == 2
