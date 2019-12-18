# Part of solution to day 13 of AOC 2019, "Care Package".
# https://adventofcode.com/2019/day/13

import game


this_game = game.Game('input.txt')
this_game.run()
# this_game.scr.render()

# "How many block tiles are on the screen when the game exits?"
block_tiles = 0
for g in this_game.scr.grid:
    if this_game.scr.grid[g] == 2:
        block_tiles += 1

print('Part 1:', block_tiles)
