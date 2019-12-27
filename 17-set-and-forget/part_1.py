# Part of solution to day 17 of AOC 2019, "Set and Forget".
# https://adventofcode.com/2019/day/17


from ascii import Ascii

this_ascii = Ascii()
this_ascii.refresh_screen()
this_ascii.render_screen()

# "What is the sum of the alignment parameters for the scaffold intersections?"
total = 0

# Check every location in the screen to see if it is an intersection.
for y in range(this_ascii.max_y + 1):
    for x in range(this_ascii.max_x + 1):
        if this_ascii.is_intersection(test_vertex=(x, y)):
            alignment_parameter = x * y
            total += alignment_parameter

print('Part 1:', total)
