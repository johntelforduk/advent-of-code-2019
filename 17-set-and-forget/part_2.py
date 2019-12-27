# Part of solution to day 17 of AOC 2019, "Set and Forget".
# https://adventofcode.com/2019/day/17


from dict_computer import Computer

comp = Computer(output_to_screen=False)
comp.load_file('input.txt')

# "Force the vacuum robot to wake up by changing the value in your ASCII program at address 0 from 1 to 2."
comp.memory[0] = 2

comp.input_from_keyboard = False
comp.output_to_screen = False

# This was deduced by playing around with check,txt in text editor
# check.txt began as copy-and-paste of output from analyse.py.
send_to_input = 'A,A,B,C,B,C,B,C,B,A\nR,6,L,6,6,R,6\nL,6,6,R,6,L,8,L,6,6\nR,6,6,L,5,5,L,5,5\nn\n'

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

print('\n\nPart 2:', comp.output)
