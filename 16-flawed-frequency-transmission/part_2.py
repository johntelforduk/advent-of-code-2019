# Part of solution to day 16 of AOC 2019, "Flawed Frequency Transmission".
# https://adventofcode.com/2019/day/16


def file_to_list_ten_thousand_times(filename: str) -> []:
    """Load the parm file into a list of single digits. Repeat this 10000 times."""
    f = open(filename, 'r')
    whole_text = f.read()
    output = []

    for i in range(10000):                      # "The real signal is your puzzle input repeated 10000 times."
        for this_digit in whole_text:
            output.append(int(this_digit))
    return output


def calculate_a_phase(input_list: []) -> []:
    """Do 1 iteration of the process."""

    input_length = len(input_list)

    running_total = 0

    # Work backwards from end of list, up to the left edge that we need for result. The -10 is a safety margin.
    # input_length - 1, is because last index of list is 1 less than length of the list.
    for element in range(input_length - 1, 5976683 - 10, -1):

        # This far right in a big signal, all multipliers are 1, so just do simple addition.
        running_total += input_list[element]

        last_digit = int(str(running_total)[-1:])
        input_list[element] = last_digit

    return input_list

# "After repeating your input signal 10000 times and running 100 phases of FFT, what is the eight-digit message
# embedded in the final output list?"

signal = file_to_list_ten_thousand_times('input.txt')

for iteration in range(100):
    print('Phase:', iteration + 1)
    signal = calculate_a_phase(signal)

# Print the 8 digits starting at 5976683.
print('Part 2: ', end='')
for digit in range(5976683, 5976683 + 8):
    print(signal[digit], end='')
