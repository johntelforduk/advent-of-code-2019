# Part of solution to day 21 of AOC 2019, "Springdroid Adventure".
# https://adventofcode.com/2019/day/21


from dict_computer import Computer

comp = Computer(output_to_screen=False)
comp.load_file('input.txt')

comp.input_from_keyboard = False

send_to_input = """NOT A J
NOT C T
AND H T
OR T J
NOT B T
AND A T
AND C T
OR T J
AND D J
RUN
"""

input_pos = 0
comp.input = ord(send_to_input[input_pos])


while not comp.halted:
    comp.run_until_io()

    # If paused due to output, turn the output into a char and send to stdout.
    if comp.new_output and comp.output < 128:   # Only print char if within range of classic ASCII chars.
        print(chr(comp.output), end='')

    if comp.new_input:                          # If paused due to input, get ASCII code for next char of input ready.
        input_pos += 1
        if input_pos < len(send_to_input):
            comp.input = ord(send_to_input[input_pos])

print('Part 2:', comp.output)