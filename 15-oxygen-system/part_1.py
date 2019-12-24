# Part of solution to day 15 of AOC 2019, "Oxygen System".
# https://adventofcode.com/2019/day/15


from oxygen_search import Search

this_search = Search()

while this_search.world.unexplored != {}:
    print('Grid size:', len(this_search.world.grid), '    Unexplored locations:', len(this_search.world.unexplored))
    this_search.explore()

this_search.world.save('world.txt')                 # We'll need a copy of world map for Part 2.
this_search.world.print(include_droid=True)

oxygen = this_search.world.oxygen_system
print('Part 1:', len(this_search.world.paths[oxygen]))
