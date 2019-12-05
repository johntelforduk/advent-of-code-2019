# Test interactive input and output, for day 5 of AOC 2019, "Sunny with a Chance of Asteroids".
# https://adventofcode.com/2019/day/5

import computer as comp

test_comp = comp.Computer(interactive_mode=True)
test_comp.memory = [3, 0, 4, 0, 99]                     # This program puts input into address 0, then outputs it.
test_comp.run()
