# Part of solution to day 17 of AOC 2019, "Set and Forget".
# https://adventofcode.com/2019/day/17


from dict_computer import Computer


# "Aft Scaffolding Control and Information Interface (ASCII, your puzzle input), provides access to the cameras
# and the vacuum robot."
class Ascii:

    def __init__(self):

        self.comp = Computer(output_to_screen=False)
        self.comp.load_file('input.txt')

        self.screen = {}                    # Key= vertex (x, y), Value= character at that vertex.
        self.max_x, self.max_y = 0, 0       # Edge positions of the screen.

        self.robot_pos = (0, 0)             # Current position of the robot.
        self.robot_direction = 'N'          # N, E, S, or W.

        self.robot_trail = []               # Steps that the robot has taken.

        self.dx = {'N': 0, 'E': 1, 'S': 0, 'W': -1}
        self.dy = {'N': -1, 'E': 0, 'S': 1, 'W': 0}

    def find_screen_edges(self):
        """Find the maximum x, and maximum y dimensions of the screen."""
        for (x, y) in self.screen:
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y

    def find_robot(self):
        """Look at all positions on the screen for the robot (caret character)."""
        for (x, y) in self.screen:
            if self.screen[(x, y)] == '^':
                self.robot_pos = (x, y)

    def refresh_screen(self):
        """Run the computer, loading its output into the screen buffer."""
        x, y = 0, 0

        while not self.comp.halted and not self.comp.input_from_keyboard:
            self.comp.run_until_output()

            if self.comp.output == 10:        # "10 starts a new line of output below the current one..."
                x = 0
                y += 1
            else:
                self.screen[(x, y)] = chr(self.comp.output)
                x += 1
        self.find_screen_edges()
        self.find_robot()

    def load_test_screen(self, filename: str):
        """Load a test screen from parm file."""
        f = open(filename, 'r')
        whole_text = f.read()
        x, y, = 0, 0

        for each_char in whole_text:
            if each_char == '\n':                        # Newline.
                x = 0
                y += 1
            else:
                self.screen[(x, y)] = each_char
                x += 1

        f.close()
        self.find_screen_edges()
        self.find_robot()

    def render_screen(self):
        """Render the screen buffer to stdout."""
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                print(self.screen[x, y], end='')
            print()

    def is_intersection(self, test_vertex: (int, int)) -> bool:
        """Is there an intersection at parm vertex?"""

        # Intersections are the centre of patterns like this,
        #   .#.
        #   ###
        #   .#.

        (test_x, test_y) = test_vertex
#        print(test_x, test_y)

        # Check that the test vertex is far enough from edges to be an intersection.
        if test_x == 0 or test_x == self.max_x or test_y == 0 or test_y == self.max_y:
            return False

        lookup = {(-1, -1): '.', (0, -1): '#', (1, -1): '.',
                  (-1, 0): '#', (0, 0): '#', (1, 0): '#',
                  (-1, 1): '.', (0, 1): '#', (1, 1): '.'}

        for check in lookup:
            (dx, dy) = check

#            print(check, lookup[check], self.screen[(test_x + dx, test_y + dy)])
            # Every lookup must match the expected value, otherwise it is not an intersection.
            if self.screen[(test_x + dx, test_y + dy)] != lookup[check]:
                return False

        # All tests passed, so it must be an intersection.
        return True

    def turn_right(self):
        """Rotate robot clockwise."""
        self.robot_direction = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[self.robot_direction]
        self.robot_trail.append('R')

    def turn_left(self):
        """Rotate robot anticlockwise."""
        self.robot_direction = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[self.robot_direction]
        self.robot_trail.append('L')

    def can_walk_one_step(self) -> bool:
        """Can the robot walk ahead 1 step without going off edge of scaffolding."""

        (x, y) = self.robot_pos

        # Check for going off edge of screen.
        if self.robot_direction == 'N' and y == 0:
            return False
        if self.robot_direction == 'W' and x == 0:
            return False
        if self.robot_direction == 'S' and y == self.max_y:
            return False
        if self.robot_direction == 'E' and x == self.max_x:
            return False

        test_pos = (x + self.dx[self.robot_direction], y + self.dy[self.robot_direction])

        if self.screen[test_pos] != '#':
            return False

        return True

    def forward(self):
        """Move forward until next step would be off edge of scaffolding."""
        step_count = 0

        while self.can_walk_one_step():
            (x, y) = self.robot_pos
            self.robot_pos = (x + self.dx[self.robot_direction], y + self.dy[self.robot_direction])
            step_count += 1

        self.robot_trail.append(str(step_count))

    def on_screen(self, test_vertex: (int, int)) -> bool:
        """Is the parm vertex within the boundaries of the screen?"""
        (test_x, test_y) = test_vertex
        if test_x < 0 or test_x > self.max_x or test_y < 0 or test_y > self.max_y:
            return False
        return True

    def seek(self) -> bool:
        """Robot has reached end of current straight bit of scaffolding. So, look left and right for next bit.
        Return false if a new direction to travel wasn't found."""

        (x, y) = self.robot_pos
        seek_left = ()
        seek_right = ()

        if self.robot_direction == 'N':
            seek_left = (x - 1, y)
            seek_right = (x + 1, y)
        if self.robot_direction == 'E':
            seek_left = (x, y - 1)
            seek_right = (x, y + 1)
        if self.robot_direction == 'S':
            seek_left = (x + 1, y)
            seek_right = (x - 1, y)
        if self.robot_direction == 'W':
            seek_left = (x, y + 1)
            seek_right = (x, y - 1)

        if self.on_screen(test_vertex=seek_left):
            if self.screen[seek_left] == '#':
                self.turn_left()
                return True

        if self.on_screen(test_vertex=seek_right):
            if self.screen[seek_right] == '#':
                self.turn_right()
                return True
