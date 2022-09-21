import pytest

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    return fib(n-1) + fib(n-2)
    
@pytest.mark.unit
def test_fib():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 2
    assert fib(3) == 3
    assert fib(4) == 5
    assert fib(5) == 8