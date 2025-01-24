import pytest

from math_operations import add, subtract


def test_add():
    assert(add(3, 2) == 5)
    assert(add(5, 6) == 11)
    assert(add(-25, 25) == 0)


def test_subtract():
    assert(subtract(10, 5) == 5)
    assert(subtract(20, 10) == 10)
    assert (subtract(6, 7) == -1)
