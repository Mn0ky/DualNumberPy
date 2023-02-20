import math

import pytest

import dmath
from DualNumber import DualNumber


def test_construction():
    assert DualNumber() == DualNumber(0)
    assert DualNumber() == 0
    assert DualNumber() == 0.0
    assert DualNumber(5) == 5
    assert DualNumber(5, 1) != 5
    assert DualNumber() == 0 + 0j
    assert DualNumber(1) == 1 + 0j == 1 == 1.0
    assert DualNumber(1, 0) == 1 + 0j == 1 == 1.0
    assert DualNumber.from_matrix([[1, 2], [0, 1]]) == DualNumber(1, 2)


def test_conversions():
    pass
    # assert complex(DualNumber(0)) == 0
    # assert DualNumber(1, 2).as_fraction_pair() == (1, 2)


def test_arithmetic():
    assert DualNumber(1) + DualNumber(2) == DualNumber(3)
    assert DualNumber(1, 2) + DualNumber(3, 4) == DualNumber(4, 6)
    assert DualNumber(1, 0) + 1 == 2
    assert DualNumber(1, 2) - DualNumber(3, 4) == DualNumber(-2, -2)
    assert DualNumber(1, 2) * DualNumber(3, 4) == DualNumber(3, 10)
    assert DualNumber(1, 2) * 2 == DualNumber(2, 4)
    assert DualNumber(1, 2) / DualNumber(3, 4) == DualNumber(1 / 3.0, 2 / 9.0)
    assert +DualNumber(1, 2) == DualNumber(1, 2)
    assert -DualNumber(1, 2) == DualNumber(-1, -2)
    assert DualNumber(1, 2).conjugate() == DualNumber(1, -2)
    assert DualNumber(1, 2) * DualNumber(1, 2).conjugate() == DualNumber(1, 2).real ** 2  # z * z* = a^2
    assert abs(DualNumber(1, 2)) == abs(1)  # abs(z) = abs(a), it is the abs value of the real component
    assert dmath.ln(DualNumber(1, 2)) == DualNumber(0, 2)
    assert dmath.log(DualNumber(1, 2)) == DualNumber(0, 2 / math.log(10))
    # TODO: Add tests for trigonometric functions


def test_operator_fallbacks():
    assert DualNumber(1) + 1 == 2
    assert type(DualNumber(1) + 1) == DualNumber

    assert 1 + DualNumber(1) == 2
    assert type(1 + DualNumber(1)) == DualNumber

    assert abs(DualNumber(1) + 1.5 - 2.5) < 1e-6    # TODO: Check in on these last 2
    assert type(DualNumber(1) + 1.5) == complex


def test_pow():
    assert DualNumber(1, 2) ** 0 == 1
    assert DualNumber(1, 2) ** 5 == DualNumber(1, 10)
    assert DualNumber(1, 2) ** -5 == DualNumber(1, -10)
    assert DualNumber(0, 1) ** 1000 == 0
    assert DualNumber(1, 2) ** 2 == DualNumber(1, 4)
    assert 2 ** DualNumber(1, 2) == DualNumber(2, 4 * math.log(2))
    assert math.e ** DualNumber(1, 2) == DualNumber(math.e, 2 * math.e)
    assert DualNumber(1, 2) ** DualNumber(1, 2) == DualNumber(1, 2)

    with pytest.raises(ZeroDivisionError):
        DualNumber(0) ** 0 == 1


def test_hash():
    assert hash(DualNumber(0)) == hash(0)
    assert hash(DualNumber(42)) == hash(42)
    assert hash(DualNumber(1 / 2)) == hash(1 / 2)
    assert hash(DualNumber(0, 1)) == hash(1j)

    d = {DualNumber(0, 1): "a", DualNumber(0): "b", DualNumber(1, 1): "c", DualNumber(1, 0): "d"}
    assert d[0] != "a"
    assert d[0] == "b"
    assert d[0j] == "b"
    assert d[1+0j] == "d"


def test_bool():
    assert not bool(DualNumber(0))
    assert bool(DualNumber(1))
    assert bool(DualNumber(0, 1))


def test_comparisons_raise():
    # For programmatic purposes, dual numbers use their real component for numerical ordering
    # although mathematically there is no defined ordering to them
    assert DualNumber(3, 5) < DualNumber(7, 1)
    assert DualNumber(1, 2) <= DualNumber(1, 2)
    assert DualNumber(1, 0) > DualNumber(0, 999)
    assert DualNumber(1, 2) >= DualNumber(1, 2)
    assert 2 > DualNumber(1, 999)
    assert 1 + 10j < DualNumber(3, 0)
