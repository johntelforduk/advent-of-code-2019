# Solution to part 1 of day 2 of AOC 2019, "1202 Program Alarm".
# https://adventofcode.com/2019/day/2

f = open('input.txt')
whole_text = (f.read())
string_list = whole_text.split(',')             # Split string by commas.

program = [int(x) for x in string_list]         # Convert list of strings to list of integers.

# ... "before running the memory, replace position 1 with the value 12 and replace position 2 with the value 2"
program[1] = 12
program[2] = 2

program_counter = 0                             # Current position of PC.
output = 0
halted = False                                  # Program is still running.

while not halted:
    opcode = program[program_counter]
    assert opcode in {1, 2, 99}                 # These are the only valid opcodes.

    if opcode == 99:
        halted = True
    else:
        arg1 = program[program[program_counter + 1]]
        arg2 = program[program[program_counter + 2]]
        output_pos = program[program_counter + 3]

        if opcode == 1:                         # Opcode 1 is addition.
            output = arg1 + arg2
        elif opcode == 2:                       # Opcode 2 is multiplication
            output = arg1 * arg2

        program[output_pos] = output
        program_counter += 4                    # Move PC four places further into the memory.

print(program[0])
