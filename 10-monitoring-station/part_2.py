# Part of solution to part 2 of day 10 of AOC 2019, "Monitoring Station".
# https://adventofcode.com/2019/day/10

from asteroid_field import AsteroidField


this_field = AsteroidField('input.txt')
this_field.station = (29, 28)                   # This was the solution to Part 1.
print('Station:', this_field.station)
this_field.flip_all()
this_field.find_targets()
this_field.targets.sort()
this_field.shoot_targets()

print('200th:', this_field.shot_order[199])
[x, y] = this_field.shot_order[199]
print('Part 2:', 100 * x + y)
