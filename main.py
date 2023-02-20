# Program that extends Python's subset of numbers by adding Dual Numbers.
# They are expressions of the form a + bε, where a and b are real numbers, and ε is a symbol taken to satisfy
# ε^n≥2 = 0 with ε ≠ 0.

# Much inspiration for how this was implemented has been taken from mCoding's video on implementing Gaussian rationals:
# https://youtu.be/lcm4tYGmAig
# As well as the following for understanding and implementing dual number operations:
# https://math.stackexchange.com/a/1056378
# https://docs.python.org/3/library/stdtypes.html
# https://docs.python.org/3/library/numbers.html
# https://alemorales.info/post/automatic-differentiation-with-dual-numbers/
# https://blog.demofox.org/2014/12/30/dual-numbers-automatic-differentiation/
# https://math.stackexchange.com/questions/900541/implementing-trig-functions-for-dual-numbers

import example_problems
from DualNumber import DualNumber


def main():
    z1 = DualNumber(3, 3)
    z2 = DualNumber(12, 4)
    print(f'Dual number multiplication: {z1 * z2}')
    print(f'Dual number multiplication by respective conjugate: {z1 * z1.conjugate()}')  # z * z* = a^2
    print(f'Dual number exponentiation: {z1 ** 2}\n')

    # For a dual number, the real component serves as its value and the imaginary component serves
    # as its initial derivative

    # Let's model the function: f(x) = x^3
    # The derivative would be: f'(x) = 3x^2
    # Let our example be f(5)

    # The example value, 5, is put as the real component
    # The initial derivative of x is 1, so that will be the imaginary component
    x = DualNumber(5, 1)
    # (Note: if f(x) was being derived with respect to x in addition to there being other variables than x, then
    # those variables would have an initial derivative of 0. Ex: dy/dx = 0, because y is not a function of x).

    print('Example function f(x) = x^3')
    output = x ** 3
    print(f'f({x.real}) output: {output}')
    print(f'f({x.real}) = {output.real}; f\'({x.real}) = {output.imag}\n')

    # The real component of the dual number has the output of f(x) and the imaginary component contains the derivative
    # of f'(x). f(5) = 5^3 = 125, f'(x) = 3*5^2 = 75

    # Example #2)
    # f(x) = ax^2 + bx + c
    # f'(x) = 2ax + b
    # Where a, b, and c are constants and = 3; x = 7

    x = DualNumber(7, 1)
    a = DualNumber(3, 0)
    b = DualNumber(3, 0)
    c = DualNumber(3, 0)
    output = a * x ** 2 + b * x + c

    print('Example function f(x) = ax^2 + bx + c')
    print(f'f({x.real}) output: {output}')
    print(f'f({x.real}) = {output.real}; f\'({x.real}) = {output.imag}\n')

    # Moving on to example problems from example_problems.py
    print("Please enter an integer to be used for the next 4 example problems.")
    z = DualNumber(int(input()), 1)

    print(f'{example_problems.r.__doc__}, at z = {z.real}: {example_problems.r(z)}')
    print(f'{example_problems.v.__doc__}, at z = {z.real}: {example_problems.v(z)}')
    print(f'{example_problems.j.__doc__}, at z = {z.real}: {example_problems.j(z)}')
    print(f'{example_problems.k.__doc__}, at z = {z.real}: {example_problems.k(z)}')
    print(f'{example_problems.p.__doc__}, at z = {z.real}: {example_problems.p(z)}')
    print("\nThis final example shows the solving of a tangent line problem.")

    print(example_problems.f.__doc__)
    output = example_problems.f()
    print(f'Solution: y - {output.real} = {output.imag}(x - 2)')


if __name__ == '__main__':
    main()
