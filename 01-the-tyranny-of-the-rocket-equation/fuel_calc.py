# Solution to day 1 of AOC 2019, The Tyranny of the Rocket Equation.
# https://adventofcode.com/2019/day/1


# Return fuel needed to lift a given mass.
# "... to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2."
def mass_to_fuel(mass):
    fuel = int(mass / 3) - 2
    if fuel < 0:                    # -ve mass requires zero fuel.
        return 0
    else:
        return fuel


# Calculate total fuel needed to lift a mass, taking into account fuel needed to lift the mass of the fuel.
def total_fuel(mass):
    this_fuel = mass_to_fuel(mass)
    if this_fuel == 0:              # Zero mass requires zero fuel.
        return 0
    else:
        return this_fuel + total_fuel(this_fuel)


f = open('input.txt')
whole_text = (f.read())
string_list = whole_text.split()                    # Split string by any whitespace.
number_list = [int(x) for x in string_list]         # Convert list of strings to list of integers.

simple_total = 0                                    # Answer to Part 1.
complex_total = 0                                   # Answer to Part 2.

for each_mass in number_list:
    simple_total += mass_to_fuel(each_mass)
    complex_total += total_fuel(each_mass)

print('Part 1:', simple_total)
print('Part 2:', complex_total)
