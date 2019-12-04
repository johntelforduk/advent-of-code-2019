# Solution to day 4 of AOC 2019, "Secure Container".
# https://adventofcode.com/2019/day/4

import fact_checks as fc

part_1, part_2 = 0, 0                               # Count of possible passwords (parts 1 & 2 of today's puzzle).
for candidate in range(152085, 670284):

    # Do the checks that apply to both part 1 & 2 first.
    if fc.is_6_digits(candidate) \
            and fc.value_in_range(number=candidate, low_bound=152085, up_bound=670283) \
            and fc.never_decrease(candidate):

        # The special tests for parts 1 & 2.
        if fc.two_adjacent_digits_same(candidate):
            part_1 += 1
        if fc.just_two_adjacent_digits_same(candidate):
            part_2 += 1

print('Part 1:', part_1)
print('Part 2:', part_2)
