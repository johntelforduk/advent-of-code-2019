# Part of solution to day 16 of AOC 2019, "Flawed Frequency Transmission".
# https://adventofcode.com/2019/day/16


def file_to_list(filename: str) -> []:
    """Load the parm file into a list of single digits."""
    f = open(filename, 'r')
    whole_text = f.read()
    output = []
    for this_digit in whole_text:
        output.append(int(this_digit))
    return output


def pattern_pos(element_number: int, position: int) -> int:
    """Return the pattern multiplier for parm element number at parm position."""
    region = (position + 1) // element_number
    quartet = region % 4
    output = [0, 1, 0, -1][quartet]
    return output


def calculate_a_phase(input_list: []) -> []:
    """Do 1 iteration of the process."""
    output = []

    input_length = len(input_list)

    for element in range(input_length):
        total = 0

        # Everything to the left of element is bound to be zero additions.
        for this_digit in range(element, input_length):
            total += input_list[this_digit] * pattern_pos(element_number=element + 1, position=this_digit)

        last_digit = int(str(total)[-1:])
        output.append(last_digit)

    return output


signal = file_to_list('input.txt')

# "After 100 phases of FFT, what are the first eight digits in the final output list?"
for iteration in range(100):
    print('Phase:', iteration + 1)
    signal = calculate_a_phase(signal)

# Print the first 8 digits.
print('Part 1: ', end='')
for digit in range(8):
    print(signal[digit], end='')
