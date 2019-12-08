# Solution to part 1 of day 7 of AOC 2019, "Amplification Circuit".
# https://adventofcode.com/2019/day/7


import computer as comp                 # From folder "04-secure-container".
import copy                             # Used to make copies of objects.

# The 'fresh' computer will never be run. It will be copied each time a computer to actually be run is needed.
fresh_computer = comp.Computer(interactive_mode=False)
fresh_computer.load('input.txt')

highest_signal = 0                              # Highest signal output found so far.

for phase_setting in range(44445):              # Range is from 00001 to 44444

    long_code = str(phase_setting).zfill(5)     # Stuff the number with leading zeros.

    # "... phase setting (an integer from 0 to 4). Each phase setting is used exactly once..."
    all_digits_ok = True
    for check in '01234':
        if check not in long_code:
            all_digits_ok = False

    if all_digits_ok:
        input_value = 0                         # Input value for first run of program is 0.

        for this_phase_setting in long_code:
            this_computer = copy.copy(fresh_computer)

            this_computer.input = int(this_phase_setting)
            this_computer.tick()
            this_computer.input = input_value
            this_computer.run_until_output()
            input_value = this_computer.output

        if this_computer.output > highest_signal:
            highest_signal = this_computer.output

print('Part 1:', highest_signal)
