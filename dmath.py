"""
This module provides access to mathematical functions supporting dual numbers. All functions derived from:
\tf(a+bε) = f(a) + bf′(a)ε
"""

import math
from DualNumber import DualNumber


def ln(z: DualNumber) -> DualNumber:
    """ln(a+bε) = ln(a) + b/aε"""
    return DualNumber(math.log(z.real), z.imag / z.real)


def log(z: DualNumber, base=10) -> DualNumber:
    """Defaults to base 10, use dmath.ln(z) for natural log.\n\nlog(a+bε) = log(a) + b/(a*log(BASE)ε"""
    return DualNumber(math.log(z.real, base), z.imag / (z.real * math.log(base)))


def sin(z: DualNumber) -> DualNumber:
    """sin(a+bε) = sin(a) + b*cos(a)ε"""
    return DualNumber(math.sin(z.real), z.imag * math.cos(z.real))


def cos(z: DualNumber) -> DualNumber:
    """cos(a+bε) = cos(a) - b*sin(a)ε"""
    return DualNumber(math.cos(z.real), -z.imag * math.sin(z.real))


def tan(z: DualNumber) -> DualNumber:
    """tan(a+bε) = tan(a) + b/cos(a)^2ε"""
    return DualNumber(math.tan(z.real), z.imag / math.cos(z.real) ** 2)


def sec(z: DualNumber) -> DualNumber:
    """sec(a+bε) = sec(a) + b/cos(a)*tan(a)ε"""
    return DualNumber(1 / math.cos(z.real), z.imag / math.cos(z.real) * math.tan(z.real))


def csc(z: DualNumber) -> DualNumber:
    """csc(a+bε) = csc(a) - b/sin(a)/tan(a)ε"""
    return DualNumber(1 / math.sin(z.real), -z.imag / math.sin(z.real) / math.tan(z.real))


def cot(z: DualNumber) -> DualNumber:
    """cot(a+bε) = cot(a) - b/sin(a)^2ε"""
    return DualNumber(1 / math.tan(z.real), -z.imag / math.sin(z.real) ** 2)


def asin(z: DualNumber) -> DualNumber:
    """arcsin(a+bε) = arcsin(a) + b/√(1-a^2)ε"""
    return DualNumber(math.asin(z.real), z.imag / math.sqrt(1 - z.real ** 2))


def acos(z: DualNumber) -> DualNumber:
    """arccos(a+bε) = arccos(a) - b/√(1-a^2)ε"""
    return DualNumber(math.acos(z.real), -z.imag / math.sqrt(1 - z.real ** 2))


def atan(z: DualNumber) -> DualNumber:
    """arctan(a+bε) = arctan(a) + b/(1+a^2)ε"""
    return DualNumber(math.atan(z.real), z.imag / (1 + z.real ** 2))


def asec(z: DualNumber) -> DualNumber:
    """arcsec(a+bε) = arcsec(a) + b/(∣a∣*√(a^2-1))ε"""
    return DualNumber(1 / math.acos(z.real), z.imag / (abs(z.real) * math.sqrt(z.real ** 2 - 1)))


def acsc(z: DualNumber) -> DualNumber:
    """arccsc(a+bε) = arccsc(a) - b/(∣a∣*√(a^2-1))ε"""
    return DualNumber(1 / math.asin(z.real), -z.imag / (abs(z.real) * math.sqrt(z.real ** 2 - 1)))


def acot(z: DualNumber) -> DualNumber:
    """arccot(a+bε) = arccot(a) - b/(a^2+1)ε"""
    return DualNumber(1 / math.atan(z.real), -z.imag / (z.real ** 2 + 1))
