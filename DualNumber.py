import math
import operator
import sys
from collections.abc import MutableSequence
from decimal import Decimal
from numbers import Rational, Complex, Real
from typing import Type


def _operator_fallbacks(monomorphic_operator, fallback_operator):
    # See https://docs.python.org/3/library/numbers.html
    def forward(a, b):
        if isinstance(b, (Rational, DualNumber)):
            return monomorphic_operator(a, b)
        elif isinstance(b, float):
            return fallback_operator(a, b)
        else:
            return NotImplemented

    forward.__name__ = f'__{fallback_operator.__name__}__'
    forward.__doc__ = monomorphic_operator.__doc__

    def reverse(b, a):
        if isinstance(a, (Rational, DualNumber)):
            return monomorphic_operator(a, b)
        elif isinstance(a, Complex):
            return fallback_operator(complex(a), complex(b))
        else:
            return NotImplemented

    reverse.__name__ = f'__r{fallback_operator.__name__}__'
    reverse.__doc__ = monomorphic_operator.__doc__

    return forward, reverse


supported_types = Rational | float | str | Decimal


class DualNumber(Complex):
    # TODO: Finish fleshing out and or reworking docs
    # TODO: Eventually switch to inheriting from Number class to improve semantics and to help dissociate from Complex
    """a + bε, where a and b are real numbers, and ε is a symbol taken to satisfy ε^2 = 0 with ε ≠ 0."""

    __slots__ = ("_real", "_imag")  # Since this object is immutable slots can be used for better memory efficiency

    def __new__(cls, real: supported_types = float(0), imag: supported_types = float(0)):
        # Use __new__ dunder for immutability
        self: DualNumber = super().__new__(cls)  # TODO: Let the type passed be the type used for real and imag
        self._real = float(real)  # When modeling f the output of f would be stored here
        self._imag = float(imag)  # When modeling f the derivative of f would be stored here

        return self

    @classmethod
    def from_matrix(cls, square_matrix: MutableSequence[MutableSequence[supported_types, supported_types],
                                                        MutableSequence[supported_types, supported_types]]):
        """Construct a dual number from a 2x2 square matrix. Will throw a TypeError if not fed a 2x2 sequence."""
        if len(square_matrix) != 2 or len(square_matrix[0]) != 2 or len(square_matrix[1]) != 2:
            return TypeError
        return cls(float(square_matrix[0][0]), float(square_matrix[0][1]))

    @classmethod
    def from_string(cls, str_expression: str):
        """Expects a string in the form of 'a + bε' and converts it to a dual number.
        The ε char in practice can be any char."""
        components = str_expression.split(" + ", 2)
        real_comp = components[0]
        imag_comp = components[1][:-1]  # Remove ε char
        return cls(float(real_comp), float(imag_comp))

    def as_matrix(self) -> list[list[Real, Real], list[Real, Real]]:
        return [[self.real, self.imag], [0, self.real]]

    def __complex__(self) -> Type[TypeError] | complex:
        """complex(self). Only works if the imaginary component of the dual number is 0."""
        if self.imag != 0:
            return TypeError  # ε ≠ i
        return float(self.real) + 0j

    def __repr__(self):
        return f'{self.__class__.__name__}({self.real!r}, {self.imag!r})'

    def __str__(self):
        return f'({self.real} + {self.imag}ε)'

    @property
    def real(self):
        return self._real

    @property
    def imag(self):
        return self._imag

    def _add(self, other):
        return DualNumber(self.real + other.real, self.imag + other.imag)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(self, other):
        return DualNumber(self.real - other.real, self.imag - other.imag)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def __neg__(self):
        return DualNumber(-self.real, -self.imag)

    def __pos__(self):
        return self

    def _mul(self, other):
        """Multiply a dual number by another dual number or a constant and vice-versa"""
        return DualNumber(self.real * other.real, self.real * other.imag + self.imag * other.real)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _truediv(self, other):
        """Divide a dual number by another dual number or a constant and vice-versa."""
        return DualNumber(self.real / other.real, (self.imag * other.real - self.real * other.imag) / other.real ** 2)

    __truediv__, __rtruediv__ = _operator_fallbacks(_truediv, operator.truediv)

    def __pow__(self, exponent):
        """
        Raise a dual number to the power of another dual number or a constant.\n
        1.) (a+bε)^(c+dε) = a^c + a^c(d*ln(a) + b*c/a)ε ✓\n
        2.) (a+bε)^n = a^n + b*n*a^(n-1) ✓\n
        (https://math.stackexchange.com/a/1914619)
        """
        if isinstance(exponent, DualNumber):
            real_component = self.real ** exponent.real
            return DualNumber(real_component, real_component * (
                    exponent.imag * math.log(self.real) + self.imag * exponent.real / self.real))

        return DualNumber(self.real ** exponent, self.imag * exponent * self.real ** (exponent - 1))

    def __rpow__(self, base):
        """
        Raise a constant to a dual number.\n
        n^(a+bε) = n^a + b*n^a*ln(n) ✓\n
        https://math.stackexchange.com/a/1914619
        """
        return DualNumber(base ** self.real, self.imag * base ** self.real * math.log(base))

    def __abs__(self):
        """
        The modulus/norm/magnitude of a dual number z = a + bε is just the absolute value of the real part |a|
        https://math.stackexchange.com/a/1056378
        """
        return abs(self.real)

    def conjugate(self):
        """a + bε -> a - bε"""
        return DualNumber(self.real, -self.imag)

    def __eq__(self, other) -> bool:
        """self == other"""
        if not isinstance(other, (Real, DualNumber)):
            if isinstance(other, Complex) and self.imag == 0 and other.imag == 0:
                return self.real == other.real
            return NotImplemented

        return self.real == other.real and self.imag == other.imag

    def __gt__(self, other):
        """> comparison uses the real component of a dual number."""
        if not isinstance(other, (Real, Complex, DualNumber)):
            return NotImplemented
        return self.real > other.real

    def __lt__(self, other):
        """< comparison uses the real component of a dual number."""
        return self.real < other.real

    def __ge__(self, other):
        """>= comparison uses the real component of a dual number."""
        return self.real >= other.real

    def __le__(self, other):
        """<= comparison uses the real component of a dual number."""
        return self.real <= other.real

    def __bool__(self) -> bool:
        """bool(self)"""
        return self.real != 0 or self.imag != 0

    def __reduce__(self):
        """Used for pickling"""
        return self.__class__, (self._real, self._imag)

    def __copy__(self):
        if type(self) == DualNumber:
            return self  # We can do this because of the immutability of DualNumber
        return self.__class__(self.real, self.imag)  # In case of subclassing

    def __deepcopy__(self, memodict={}):
        if type(self) == DualNumber:
            return self  # We can do this because of the immutability of DualNumber
        return self.__class__(self.real, self.imag)  # In case of subclassing

    def __hash__(self) -> int:
        """
        Compute the hash of a complex number z.
        Derived from: https://docs.python.org/3/library/stdtypes.html#hashing-of-numeric-types
        """
        hash_value = hash(self.real) + sys.hash_info.imag * hash(self.imag)

        # do a signed reduction modulo 2**sys.hash_info.width
        M = 2 ** (sys.hash_info.width - 1)
        hash_value = (hash_value & (M - 1)) - (hash_value & M)
        if hash_value == -1:
            hash_value = -2

        return hash_value
