# -*- coding: utf-8 -*-

from enforcer import enforce, TypeViolationError

import pytest

@enforce
def safe_doubler(x):
    y: int = x * 2
    return y

def test_safe():
    with pytest.raises(TypeViolationError):
        safe_doubler('1')
