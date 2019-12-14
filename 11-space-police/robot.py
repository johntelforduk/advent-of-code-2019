# Solution to day 11 of AOC 2019, "Space Police".
# https://adventofcode.com/2019/day/11

import dict_computer as comp


class Robot:

    def __init__(self):

        self.computer = comp.Computer(interactive_mode=False)
        self.computer.load_file(filename='input.txt')

        self.location = (0, 0)          # Current location of the robot.
        self.bearing = 'N'              # Direction that robot is currently pointing in. "The robot starts facing up."

    def turn_left(self):
        left_turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.bearing = left_turns[self.bearing]

    def turn_right(self):
        left_turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.bearing = left_turns[self.bearing]

    def forward(self):
        (x, y) = self.location

        dx = {'W': -1, 'E': 1, 'N': 0, 'S': 0}
        dy = {'N': -1, 'S': 1, 'E': 0, 'W': 0}

        self.location = (x + dx[self.bearing], y + dy[self.bearing])


this_robot = Robot()

# Key = tuple (x, y) of location of panel, value is colour of panel.
hull = dict()

hull[this_robot.location] = 1          # Part 2: "After starting the robot on a single white panel instead..."

while this_robot.computer.halted is False:

    # "The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel
    # or 1 if the robot is over a white panel."

    this_robot.computer.input = hull.get(this_robot.location, 0)      # By default, panels are black ('0').

    # "First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the
    # panel black, and 1 means to paint the panel white."

    this_robot.computer.run_until_output()
    assert this_robot.computer.output in {0, 1}             # '0' is paint it black, '1' is paint it white.
    hull[this_robot.location] = this_robot.computer.output

    # Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90
    # degrees, and 1 means it should turn right 90 degrees.

    this_robot.computer.run_until_output()
    assert this_robot.computer.output in {0, 1}             # '0 is turn left, '1' is turn right.
    if this_robot.computer.output == 0:
        this_robot.turn_left()
    else:
        this_robot.turn_right()

    # After the robot turns, it should always move forward exactly one panel.
    this_robot.forward()

print('Part 1:', len(hull))

# Print the image.
for y in range(10):
    for x in range(45):
        panel = hull.get((x, y), 0)

        if panel == 1:
            print('#', end='')
        else:
            print(' ', end='')
    print()
