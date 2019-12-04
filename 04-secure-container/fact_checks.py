# Part of solution to day 4 of AOC 2019, "Secure Container".
# https://adventofcode.com/2019/day/4


def is_6_digits(number:int) -> bool:
    """It is a six-digit number."""
    if len(str(number)) == 6:
        return True
    else:
        return False


def value_in_range(number:int, low_bound:int, up_bound:int) -> bool:
    """The value is within the range given in your puzzle input."""
    if low_bound <= number <= up_bound:
        return True
    else:
        return False

