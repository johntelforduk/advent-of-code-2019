# Part of solution to day 12 of AOC 2019, "The N-Body Problem".
# https://adventofcode.com/2019/day/12


import jovian_system as jovian


this_system = jovian.JovianSystem()
this_system.load_file('input.txt')

print(this_system.pos)
print(this_system.vel)
this_system.print()

for steps in range(1000):
    this_system.time_step()
    this_system.print()

this_system.print_energy()
