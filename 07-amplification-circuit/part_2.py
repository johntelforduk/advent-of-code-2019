# Solution to part 2 of day 7 of AOC 2019, "Amplification Circuit".
# https://adventofcode.com/2019/day/7


import computer as comp                 # From folder "04-secure-container".

highest_output = 0

for phase_setting in range(50000, 100000):      # 50000 to 99999
    long_code = str(phase_setting).zfill(5)         # Stuff the number with leading zeros.

    # "... phase setting (an integer from 5 to 9). Each phase setting is used exactly once..."
    all_digits_ok = True
    for check in '56789':
        if check not in long_code:
            all_digits_ok = False

    if all_digits_ok:
        # Make a list of 5 computers.
        computers = []
        for this_phase_setting in long_code:
            this_computer = comp.Computer(interactive_mode=False)
            this_computer.load('input.txt')

            this_computer.input = int(this_phase_setting)
            this_computer.tick()

            computers.append(this_computer)

        # Set the input of 1st computer to 0.
        computers[0].input = 0

        curr_comp = 0                       # Number of computer currently running.
        count_halted = 0                    # How many of the computers are halted?

        while count_halted == 0:            # Stop feedback loop when all 5 computers are halted.
            computers[curr_comp].run_until_output()
            seed = computers[curr_comp].output

            curr_comp += 1                  # Rotate current computer through 0 to 4.
            if curr_comp > 4:
                curr_comp = 0

            # New current computer's input is set to the output of previous current computer.
            computers[curr_comp].input = seed

            count_halted = 0
            for c in computers:
                if c.halted:
                    count_halted += 1

        if computers[4].output > highest_output:
            highest_output = computers[4].output

print('Part 2:', highest_output)
