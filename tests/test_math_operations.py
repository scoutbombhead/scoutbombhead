import pytest

import sys
import os

# Add the directory containing 'Python_scripts_to_test' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Python_scripts_to_test.math_operations import add, subtract


def test_add():
    assert(add(3, 2) == 5)
    assert(add(5, 6) == 11)
    assert(add(-25, 25) == 0)


def test_subtract():
    assert(subtract(10, 5) == 5)
    assert(subtract(20, 10) == 10)
    assert (subtract(6, 7) == -1)
