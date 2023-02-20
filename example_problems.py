import math
import dmath

from DualNumber import DualNumber


# TODO: Find local min/maxes
# Problem #1
# https://tutorial.math.lamar.edu/Solutions/CalcI/ChainRule/Prob4.aspx
def r(z: DualNumber) -> DualNumber:
    """r(z) = csc(7z)"""
    return -7 * dmath.csc(7 * z)


# Problem #2
# https://tutorial.math.lamar.edu/Solutions/CalcI/ChainRule/Prob12.aspx
def v(z: DualNumber) -> DualNumber:
    """v(z) = ln(sin(z) - cot(z))"""
    return dmath.ln(dmath.sin(z) - dmath.cot(z))


# Problem #3
def j(z: DualNumber) -> DualNumber:
    """j(z) = 4(2)^z"""
    return 4 * 2 ** z


# Problem #4
def k(z: DualNumber) -> DualNumber:
    """k(z) = 4(z)^z"""
    return 4 * z ** z


# Problem #5
# https://tutorial.math.lamar.edu/Solutions/CalcI/ChainRule/Prob27.aspx
def p(z: DualNumber) -> DualNumber:
    """p(x) = (3_√(12x) + sin^2(3x))^−1"""
    return ((12 * z) ** (1 / 3) + (dmath.sin(3 * z)) ** 2) ** -1


# Problem #6
# https://tutorial.math.lamar.edu/Solutions/CalcI/ChainRule/Prob28.aspx
def f(z: DualNumber = DualNumber(2, 1)) -> DualNumber:
    """Find the tangent line to f(z) = 4√(2z) − 6e^(2 − z) at z = 2."""
    return 4 * (2 * z) ** .5 - 6 * math.e ** (2 - z)
