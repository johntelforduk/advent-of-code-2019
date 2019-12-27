# Part of solution to day 9 of AOC 2019, "Sensor Boost".
# This computer has memory implemented as a dictionary. (Previous version had list for memory). This is to allow
# much bigger addressable memory.
# https://adventofcode.com/2019/day/9


class Computer:

    def __init__(self, output_to_screen: bool):
        """Boot up a new computer."""

        # True means that input is read from keyboard, and stdout is printed.
        self.output_to_screen = output_to_screen
        self.input_from_keyboard = output_to_screen     # Good default for this.

        self.memory = {}                    # The computer's memory is a dictionary.
        self.instruction_pointer = 0        # Current position of instruction pointer.
        self.relative_base = 0              # Used for Relative Mode parms.

        self.parms = []                     # List of parms for current instruction.
        self.parm_modes = []                # For each parm, 0 = position mode, 1 = immediate mode.
        self.branched = False               # Did the current instruction cause the program to branch?

        self.halted = False                 # Program is still running.
        self.input, self.output = 0, 0      # Most recent input and output from the computer.

        self.new_input = False              # True whenever the computer takes new input.
        self.new_output = False             # True whenever the computer produces new output.

    def load_list(self, program_list: []):
        """Load parm list of integers into computer memory."""
        address = 0
        for value in program_list:
            self.memory[address] = int(value)
            address += 1

    def load_file(self, filename: str):
        """Load a program from parm filename into the memory of the computer."""
        f = open(filename)
        whole_text = (f.read())
        string_list = whole_text.split(',')                         # Split string by commas.
        memory_list = [int(x) for x in string_list]                 # Convert list of strings to list of integers.
        f.close()
        self.load_list(memory_list)

    def parm_value(self, parm_number: int) -> int:
        """For the parameter parm number (0 to 2), return the correct value.
        Value will be either based on position, immediate or relative mode."""

        assert parm_number in {0, 1}                                # Only the first 2 parms can be read from.

        this_parm_mode = self.parm_modes[parm_number]

        # 0 is position mode, 1 is immediate mode. 2 is relative mode. There are no other modes.
        assert this_parm_mode in {0, 1, 2}

        if self.parm_modes[parm_number] == 0:
            return self.memory.get(self.parms[parm_number], 0)                          # 0 is position mode.
        elif self.parm_modes[parm_number] == 1:
            return self.parms[parm_number]                                              # 1 is immediate mode
        else:
            return self.memory.get(self.parms[parm_number] + self.relative_base, 0)     # 2 is relative mode.

    def assign_to_target(self, parm_number: int, assignment: int):
        """Assign value to the address found using parameter parm number."""

        assert self.parm_modes[parm_number] in {0, 2}   # Assigments can only be position or relative mode.

        if self.parm_modes[parm_number] == 0:                                           # 0 is Position mode.
            self.memory[self.parms[parm_number]] = assignment
        else:                                                                           # 2 is Relative mode.
            self.memory[self.parms[parm_number] + self.relative_base] = assignment

    def add(self):
        self.assign_to_target(parm_number=2, assignment=self.parm_value(0) + self.parm_value(1))

    def multiply(self):
        self.assign_to_target(parm_number=2, assignment=self.parm_value(0) * self.parm_value(1))

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
            self.assign_to_target(parm_number=2, assignment=1)
        else:
            self.assign_to_target(parm_number=2, assignment=0)

    def equals(self):
        """if the first parameter is equal to the second parameter, it stores 1 in the position given by the third
        parameter. Otherwise, it stores 0."""
        if self.parm_value(0) == self.parm_value(1):
            self.assign_to_target(parm_number=2, assignment=1)
        else:
            self.assign_to_target(parm_number=2, assignment=0)

    def take_input(self):
        """Opcode 3 takes a single integer as input and saves it to the position given by its only parameter.
        For example, the instruction 3, 50 would take an input value and store it at address 50."""
        if self.input_from_keyboard:
            print('Input: ', end='')
            self.input = int(input())
        self.assign_to_target(parm_number=0, assignment=self.input)
        self.new_input = True

    def emit_output(self):
        """Opcode 4 outputs the value of its only parameter.
        For example, the instruction 4, 50 would output the value at address 50."""
        self.output = self.parm_value(0)
        self.new_output = True                      # Flag that new output has been produced.
        if self.output_to_screen:
            print("Output:", self.output)

    def adjust_relative_base(self):
        """Opcode 9 adjusts the relative base by the value of its only parameter.
        The relative base increases (or decreases, if the value is negative) by the value of the parameter."""
        self.relative_base += self.parm_value(0)

    def halt(self):
        """Halt the program."""
        self.halted = True

    def tick(self):
        """Execute the next instruction."""

        # Reset the branched attribute. If this operation causes a branch, it will be set to True.
        self.branched = False
        self.new_input = False
        self.new_output = False

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
        assert opcode in {1, 2, 3, 4, 5, 6, 7, 8, 9, 99}               # These are the only valid opcodes.

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
                          9: (self.adjust_relative_base, 2),
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

    # def run_until_input(self):
    #     """Run program until it either produces prompts for some input, or it halts."""
    #     # Reset the new input produced attribute. If new input is  is emitted, it will ne set to True.
    #     self.new_input = False
    #
    #     while not self.new_output and not self.halted:
    #         self.tick()

    def run_until_io(self):
        """Run program until it either produces some input, or output, or it halts."""
        # Reset the new input and output produced attributes.
        self.new_input = False
        self.new_output = False

        while not self.new_input and not self.new_output and not self.halted:
            self.tick()

    def dump(self):
        """Print contents of important attributes."""
        print(self.memory)
        print('IP:', self.instruction_pointer,
              'Instruction:', self.memory[self.instruction_pointer],
              'Relative Base:', self.relative_base,
              'Input:', self.input,
              'Output:', self.output,
              'Halted:', self.halted)
