# Solution to part 2 of day 2 of AOC 2019, "1202 Program Alarm".
# https://adventofcode.com/2019/day/2

f = open('input.txt')
whole_text = (f.read())
string_list = whole_text.split(',')                     # Split string by commas.

program = [int(x) for x in string_list]                 # Convert list of strings to list of integers.

noun_verb = None                                        # Result of 100 * noun + verb.

for noun in range(100):
    for verb in range(100):
        memory = program.copy()                         # Re-initialise the computer's memory.

        memory[1] = noun                                # Overwrite some memory with loop vars.
        memory[2] = verb

        instruction_pointer = 0                         # Current position of PC.
        output = 0
        halted = False                                  # Program is still running.

        while not halted:
            opcode = memory[instruction_pointer]

            assert opcode in {1, 2, 99}                 # These are the only valid opcodes.

            if opcode == 99:
                halted = True
            else:
                parm1 = memory[memory[instruction_pointer + 1]]
                parm2 = memory[memory[instruction_pointer + 2]]
                output_pos = memory[instruction_pointer + 3]

                if opcode == 1:                         # Opcode 1 is addition.
                    output = parm1 + parm2
                elif opcode == 2:                       # Opcode 2 is multiplication
                    output = parm1 * parm2

                memory[output_pos] = output
                instruction_pointer += 4                # Move PC four places further into the memory.

        if memory[0] == 19690720:
            noun_verb = 100 * noun + verb
            break
    if noun_verb is not None:
        break

print(noun_verb)
