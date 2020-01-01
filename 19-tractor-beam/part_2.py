# Part of solution to day 19 of AOC 2019, "Tractor Beam".
# https://adventofcode.com/2019/day/19

from dict_computer import Computer


# "How many points are affected by the tractor beam in the 50x50 area closest to the emitter?
# (For each of X and Y, this will be 0 through 49.)

ship_size = 100

ship_x = 261
ship_y = 980


for y in range(975, 1100):
    for x in range(220, 380):
        this_comp = Computer(output_to_screen=False)
        this_comp.load_file('input.txt')

        this_comp.input = x
        this_comp.run_until_io()

        this_comp.input = y
        this_comp.run()

        ship_area = (ship_x <= x < ship_x + ship_size and ship_y <= y < ship_y + ship_size)
        if ship_area and this_comp.output == 1:
            display = 'O'
        elif ship_area and this_comp.output == 0:
            display = 'o'
        elif this_comp.output == 1:
            display = '#'
        else:
            display = '.'

        print(display, end='')
    print()

# What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate?
print('Part 2:', 10000 * ship_x + ship_y)
