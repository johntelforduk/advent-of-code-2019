# Part of solution to day 18 of AOC 2019, "Many-Worlds Interpretation".
# https://adventofcode.com/2019/day/18

from key_world import KeyWorld


this_world = KeyWorld('input.txt')
this_world.find_all_shortest_routes()
this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
print('Part 1:', this_world.shortest_route_steps)
