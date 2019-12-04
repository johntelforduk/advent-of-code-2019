# Unit tests for day 4 of AOC 2019, "Secure Container".
# https://adventofcode.com/2019/day/4

import fact_checks as fc
import unittest             # These tests based on, https://docs.python.org/3/library/unittest.html


class TestIs6Digits(unittest.TestCase):

    def test_is_6_digit(self):
        self.assertFalse(fc.is_6_digits(0))
        self.assertFalse(fc.is_6_digits(12345))
        self.assertFalse(fc.is_6_digits(1234567))
        self.assertTrue(fc.is_6_digits(123456))
        self.assertTrue(fc.is_6_digits(100000))
        self.assertTrue(fc.is_6_digits(999999))

    def test_value_in_range(self):
        self.assertFalse(fc.value_in_range(number=5, low_bound=6, up_bound=20))
        self.assertFalse(fc.value_in_range(number=5, low_bound=1, up_bound=4))
        self.assertTrue(fc.value_in_range(number=5, low_bound=4, up_bound=10))
        self.assertTrue(fc.value_in_range(number=5, low_bound=5, up_bound=10))
        self.assertTrue(fc.value_in_range(number=5, low_bound=1, up_bound=6))
        self.assertTrue(fc.value_in_range(number=5, low_bound=1, up_bound=5))

    def test_adjacent_digits_same(self):
        self.assertFalse(fc.two_adjacent_digits_same(123789))
        self.assertTrue(fc.two_adjacent_digits_same(122345))
        self.assertTrue(fc.two_adjacent_digits_same(111111))

    def test_just_two_adjacent_digits_same(self):
        self.assertFalse(fc.just_two_adjacent_digits_same(123444))
        self.assertFalse(fc.just_two_adjacent_digits_same(222346))
        self.assertFalse(fc.just_two_adjacent_digits_same(233346))
        self.assertTrue(fc.just_two_adjacent_digits_same(112233))
        self.assertTrue(fc.just_two_adjacent_digits_same(111122))
        self.assertTrue(fc.just_two_adjacent_digits_same(112345))
        self.assertTrue(fc.just_two_adjacent_digits_same(123455))
        self.assertTrue(fc.just_two_adjacent_digits_same(122456))

    def test_never_decrease(self):
        self.assertFalse(fc.never_decrease(223450))
        self.assertTrue(fc.never_decrease(122345))
        self.assertTrue(fc.never_decrease(111111))


if __name__ == '__main__':
    unittest.main()
