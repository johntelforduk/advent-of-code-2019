# Part of solution to day 5 of AOC 2019, "Sunny with a Chance of Asteroids".
# https://adventofcode.com/2019/day/5


class Computer:

    def __init__(self, interactive_mode: bool):
        """Boot up a new computer."""

        # True means that input is read from keyboard, and stdout is printed.
        self.interactive_mode = interactive_mode

        self.memory = []                    # The computer's memory is a list of integers.
        self.instruction_pointer = 0        # Current position of instruction pointer.

        self.parms = []                     # List of parms for current instruction.
        self.parm_modes = []                # For each parm, 0 = position mode, 1 = immediate mode.
        self.branched = False               # Did the current instruction cause the program to branch?

        self.halted = False                 # Program is still running.
        self.input, self.output = 0, 0      # Most recent input and output from the computer.
        self.new_output = False             # True whenever the computer produces new output.

    def load(self, filename: str):
        """Load a program from parm filename into the memory of the computer."""
        f = open(filename)
        whole_text = (f.read())
        string_list = whole_text.split(',')                         # Split string by commas.
        self.memory = [int(x) for x in string_list]                 # Convert list of strings to list of integers.
        f.close()

    def parm_value(self, parm_number: int) -> int:
        """For the parameter parm number (0 to 2), return the correct value.
        Value will be either based on position mode or immediate mode."""

        assert parm_number in {0, 1}                                # Only the first 2 parms can be read from.

        this_parm_mode = self.parm_modes[parm_number]
        assert this_parm_mode in {0, 1}             # 0 is position mode, 1 is immediate mode. There are no other modes.

        if self.parm_modes[parm_number] == 0:
            return self.memory[self.parms[parm_number]]             # 0 is position mode.
        else:
            return self.parms[parm_number]                          # 1 is immediate mode

    def add(self):
        self.memory[self.parms[2]] = self.parm_value(0) + self.parm_value(1)

    def multiply(self):
        self.memory[self.parms[2]] = self.parm_value(0) * self.parm_value(1)

    def jump_if_true(self):
        """If the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing."""
        if self.parm_value(0) != 0:
            self.instruction_pointer = self.parm_value(1)
            self.branched = True

    def jump_if_false(self):
        """If the first parameter is zero, it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing."""
        if self.parm_value(0) == 0:
            self.instruction_pointer = self.parm_value(1)
            self.branched = True

    def less_than(self):
        """If the first parameter is less than the second parameter, it stores 1 in the position given by the third
        parameter. Otherwise, it stores 0."""
        if self.parm_value(0) < self.parm_value(1):
            self.memory[self.parms[2]] = 1
        else:
            self.memory[self.parms[2]] = 0

    def equals(self):
        """if the first parameter is equal to the second parameter, it stores 1 in the position given by the third
        parameter. Otherwise, it stores 0."""
        if self.parm_value(0) == self.parm_value(1):
            self.memory[self.parms[2]] = 1
        else:
            self.memory[self.parms[2]] = 0

    def take_input(self):
        """Opcode 3 takes a single integer as input and saves it to the position given by its only parameter.
        For example, the instruction 3, 50 would take an input value and store it at address 50."""
        if self.interactive_mode:
            print('Input: ', end='')
            self.input = int(input())
        self.memory[self.parms[0]] = self.input

    def emit_output(self):
        """Opcode 4 outputs the value of its only parameter.
        For example, the instruction 4, 50 would output the value at address 50."""
        self.output = self.parm_value(0)
        self.new_output = True                      # Flag that new output has been produced.
        if self.interactive_mode:
            print("Output:", self.output)

    def halt(self):
        """Halt the program."""
        self.halted = True

    def tick(self):
        """Execute the next instruction."""

        # Reset the branched attribute. If this operation causes a branch, it will be set to True.
        self.branched = False

        # Left pad the code with leading zeros to make it five chars long.
        long_code = str(self.memory[self.instruction_pointer]).zfill(5)

        # For example,
        # ABCDE
        # 01002
        #
        # DE - two-digit opcode,      02 == opcode 2
        # C - mode of 1st parameter,  0 == position mode
        # B - mode of 2nd parameter,  1 == immediate mode
        # A - mode of 3rd parameter,  0 == position mode,

        opcode = int(long_code[3:5])
        assert opcode in {1, 2, 3, 4, 5, 6, 7, 8, 99}               # These are the only valid opcodes.

        # Key = opcode, value = (function to execute the function, length of the instruction).
        # Length of the instruction includes the opcode.
        opcode_to_func = {1: (self.add, 4),
                          2: (self.multiply, 4),
                          3: (self.take_input, 2),
                          4: (self.emit_output, 2),
                          5: (self.jump_if_true, 3),
                          6: (self.jump_if_false, 3),
                          7: (self.less_than, 4),
                          8: (self.equals, 4),
                          99: (self.halt, 1)}

        (this_function, values_in_instruction) = opcode_to_func.get(opcode)

        # Set parms and parm modes according to length of instruction.
        self.parms = []                                             # Reset parms list.
        self.parm_modes = []                                        # Reset parm modes list.

        if values_in_instruction > 1:                               # Single value instruction have no parms.
            for p in range(values_in_instruction - 1):              # One less parm than length of instruction.
                self.parms.append(self.memory[self.instruction_pointer + p + 1])
                self.parm_modes.append(int(long_code[2 - p]))

        # Execute the current instruction.
        this_function()

        # Advance to the next instruction, unless the current instruction caused a branch.
        if not self.branched:
            self.instruction_pointer += values_in_instruction

    def run(self):
        """Run program. Start at position of instruction pointer. End when program halts."""
        while not self.halted:
            self.tick()

    def run_until_output(self):
        """Run program until it either produces some output, or it halts."""
        # Reset the new output produced attribute. If new output is emitted, it will ne set to True.
        self.new_output = False

        while not self.new_output and not self.halted:
            self.tick()

    def dump(self):
        """Print contents of important attributes."""
        print('IP:', self.instruction_pointer, 'Input:', self.input, 'Output:', self.output, 'Halted:', self.halted)
