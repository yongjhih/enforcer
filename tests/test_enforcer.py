# -*- coding: utf-8 -*-

from enforcer import enforce, TypeViolationError

import pytest

@enforce
def safe_doubler(x):
    y: int = x * 2
    return y

def test_safe_error():
    with pytest.raises(TypeViolationError):
        safe_doubler('1')

def test_safe():
    assert safe_doubler(1) == 2
