# Part of solution to day 19 of AOC 2019, "Tractor Beam".
# https://adventofcode.com/2019/day/19

from dict_computer import Computer


# "How many points are affected by the tractor beam in the 50x50 area closest to the emitter?
# (For each of X and Y, this will be 0 through 49.)

points = 0

for y in range(50):
    for x in range(50):
        this_comp = Computer(output_to_screen=False)
        this_comp.load_file('input.txt')

        this_comp.input = x
        this_comp.run_until_io()

        this_comp.input = y
        this_comp.run()

        if this_comp.output == 1:
            points += 1

        print(this_comp.output, end='')
    print()

print('Part 1:', points)
