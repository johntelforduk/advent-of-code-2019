# Part of solution to day 13 of AOC 2019, "Care Package".
# https://adventofcode.com/2019/day/13

import game


this_game = game.Game('input.txt')

# Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.
this_game.comp.memory[0] = 2

this_game.comp.input_from_keyboard = False              # Change this to True to control the paddle using keyboard.
this_game.comp.output_to_screen = False                 # Output from computer is interpreted into screen updates.

this_game.run()
