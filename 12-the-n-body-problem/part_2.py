# Part of solution to day 12 of AOC 2019, "The N-Body Problem".
# https://adventofcode.com/2019/day/12


import jovian_system as jovian

this_system = jovian.JovianSystem()
this_system.load_file('input.txt')

this_system.find_matches()
