# Part of solution to day 15 of AOC 2019, "Oxygen System".
# https://adventofcode.com/2019/day/15


from oxygen_search import World
from copy import deepcopy

this_world = World()
this_world.load(filename='world.txt')           # File produced by part_1.
this_world.print(include_droid=False)

oxygen = [this_world.oxygen_system]             # List of places with Oxygen

alpha = [this_world.oxygen_system]
beta = []
minutes = 0

while len(alpha) != 0:
    for (x, y) in alpha:
        # Look in all directions from this place for available space.

        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            check_x = x + dx
            check_y = y + dy

            check_location = (check_x, check_y)

            # Oxygen can only go into grid locations that robot previously found.
            if check_location in this_world.grid:

                # If the location doesn't have oxygen in it already, and it is not wall.
                if check_location not in oxygen and this_world.grid[check_location] == 1:
                    beta.append(check_location)
                    oxygen.append(check_location)

    # Copy beta to alpha, and reset beta.
    alpha = deepcopy(beta)
    beta = []

    if len(alpha) > 0:
        minutes += 1

print('Part 2:', minutes)
