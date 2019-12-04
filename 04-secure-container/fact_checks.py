# Part of solution to day 4 of AOC 2019, "Secure Container".
# https://adventofcode.com/2019/day/4


def is_6_digits(number: int) -> bool:
    """It is a six-digit number."""
    if len(str(number)) == 6:
        return True
    return False


def value_in_range(number: int, low_bound: int, up_bound: int) -> bool:
    """The value is within the range given in your puzzle input."""
    if low_bound <= number <= up_bound:
        return True
    return False


def two_adjacent_digits_same(number: int) -> bool:
    """Two adjacent digits are the same (like 22 in 122345)."""
    previous = None
    for digit in str(number):
        if digit == previous:
            return True
        previous = digit
    return False


def just_two_adjacent_digits_same(number: int) -> bool:
    """Two adjacent matching digits are not part of a larger group of matching digits."""
    digits = str(number)
    num_length = len(digits)

    for pair in range(num_length - 1):          # For example, a 6 digit number has 5 pairs to check.

        d1 = digits[pair]                       # First digit of the pair.
        d2 = digits[pair + 1]                   # Second digit of the pair.

        if pair != 0:
            d0 = digits[pair - 1]               # Digit to the left of the first digit.
        else:
            d0 = None                           # There is no digit to the left of the first digit.

        if pair != num_length - 2:
            d3 = digits[pair + 2]               # Digit to the right of the second digit.
        else:
            d3 = None                           # There is no digit to the right of the last digit.

        if d1 == d2 and d0 != d1 and d2 != d3:
            return True
    return False


def never_decrease(number: int) -> bool:
    """Going from left to right, the digits never decrease;
    they only ever increase or stay the same (like 111123 or 135679)."""
    previous = None
    for digit in str(number):
        if previous is not None and digit < previous:
            return False
        previous = digit
    return True
