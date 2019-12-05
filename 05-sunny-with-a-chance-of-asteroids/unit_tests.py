# Unit tests for day 5 of AOC 2019, "Sunny with a Chance of Asteroids".
# https://adventofcode.com/2019/day/5

import computer as comp
import unittest


class TestComputer(unittest.TestCase):

    def test_add(self):
        test_comp = comp.Computer(interactive_mode=False)
        test_comp.memory = [1, 0, 0, 0, 99]             # (1 + 1 = 2)
        self.assertEqual(test_comp.memory[0], 1)            # Before program is run, memory[0] should be 1.
        test_comp.run()
        self.assertEqual(test_comp.memory[0], 2)

    def test_multiply(self):
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [2, 3, 0, 3, 99]             # (3 * 2 = 6)
        self.assertEqual(test_comp1.memory[3], 3)            # Before program is run, memory[3] should be 3.
        test_comp1.run()
        self.assertEqual(test_comp1.memory[3], 6)

        test_comp2 = comp.Computer(interactive_mode=False)
        test_comp2.memory = [2, 4, 4, 5, 99, 0]             # (99 * 99 = 9801)
        self.assertEqual(test_comp2.memory[5], 0)            # Before program is run, memory[5] should be 0.
        test_comp2.run()
        self.assertEqual(test_comp2.memory[5], 9801)

    def test_complex_programs(self):
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
        self.assertEqual(test_comp1.memory[0], 1)
        test_comp1.run()
        self.assertEqual(test_comp1.memory[0], 3500)

        test_comp2 = comp.Computer(interactive_mode=False)
        test_comp2.memory = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        self.assertEqual(test_comp2.memory[0], 1)
        test_comp2.run()
        self.assertEqual(test_comp2.memory[0], 30)

    def test_input_output(self):
        test_comp = comp.Computer(interactive_mode=False)
        test_comp.memory = [3, 0, 4, 0, 99]                 # This program puts input into address 0, then outputs it.
        test_comp.input = 7
        self.assertEqual(test_comp.output, 0)            # Before program is run, output should be 0.
        test_comp.run()
        self.assertEqual(test_comp.output, 7)

    def test_conditionals(self):
        # 3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is)
        # or 0 (if it is not).
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        test_comp1.input = 8
        test_comp1.run()
        self.assertEqual(test_comp1.output, 1)
        test_comp2 = comp.Computer(interactive_mode=False)
        test_comp2.memory = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        test_comp2.input = 9                    # This is not 8.
        test_comp2.run()
        self.assertEqual(test_comp2.output, 0)

        # 3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it
        # is) or 0 (if it is not).
        test_comp3 = comp.Computer(interactive_mode=False)
        test_comp3.memory = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        test_comp3.input = 7                    # This is less than 8.
        test_comp3.run()
        self.assertEqual(test_comp3.output, 1)
        test_comp4 = comp.Computer(interactive_mode=False)
        test_comp4.memory = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        test_comp4.input = 9                    # This is not less than 8.
        test_comp4.run()
        self.assertEqual(test_comp4.output, 0)

        # 3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is)
        # or 0 (if it is not).
        test_comp5 = comp.Computer(interactive_mode=False)
        test_comp5.memory = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        test_comp5.input = 8
        test_comp5.run()
        self.assertEqual(test_comp5.output, 1)
        test_comp6 = comp.Computer(interactive_mode=False)
        test_comp6.memory = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        test_comp6.input = 3                    # This is not 8.
        test_comp6.run()
        self.assertEqual(test_comp6.output, 0)

        # 3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is)
        # or 0 (if it is not).
        test_comp7 = comp.Computer(interactive_mode=False)
        test_comp7.memory = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        test_comp7.input = 5                    # This is less than 8.
        test_comp7.run()
        self.assertEqual(test_comp7.output, 1)
        test_comp8 = comp.Computer(interactive_mode=False)
        test_comp8.memory = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        test_comp8.input = 20                   # This is greater than 8.
        test_comp8.run()
        self.assertEqual(test_comp8.output, 0)

    def test_jumping(self):
        # Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was
        # non-zero:
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        test_comp1.input = 0
        test_comp1.run()
        self.assertEqual(test_comp1.output, 0)
        test_comp2 = comp.Computer(interactive_mode=False)
        test_comp2.memory = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        test_comp2.input = 4                            # Non-zero.
        test_comp2.run()
        self.assertEqual(test_comp2.output, 1)
        test_comp3 = comp.Computer(interactive_mode=False)
        test_comp3.memory = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        test_comp3.input = 0
        test_comp3.run()
        self.assertEqual(test_comp3.output, 0)
        test_comp4 = comp.Computer(interactive_mode=False)
        test_comp4.memory = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        test_comp4.input = 4                            # Non-zero.
        test_comp4.run()
        self.assertEqual(test_comp4.output, 1)

    def test_large_example(self):
        # Uses an input instruction to ask for a single number. The program will then output 999 if the input value is
        # below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                             1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                             999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        test_comp1.input = 7                            # Below 8.
        test_comp1.run()
        self.assertEqual(test_comp1.output, 999)

    def test_day_2_program(self):
        test_comp = comp.Computer(interactive_mode=False)
        test_comp.load('day_2_program.txt')

        # "Replace position 1 with the value 12 and replace position 2 with the value 2"
        test_comp.memory[1] = 12
        test_comp.memory[2] = 2

        test_comp.run()
        self.assertEqual(test_comp.memory[0], 5482655)          # This was the solution to Part 1 of Day 2.

    def test_immediate_mode(self):
        test_comp1 = comp.Computer(interactive_mode=False)
        test_comp1.memory = [1002, 4, 3, 4, 33]
        self.assertEqual(test_comp1.memory[4], 33)
        test_comp1.run()
        self.assertEqual(test_comp1.memory[4], 99)


if __name__ == '__main__':
    unittest.main()
