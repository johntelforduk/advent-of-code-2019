# Part of solution to day 20 of AOC 2019, "Donut Maze".
# https://adventofcode.com/2019/day/20


from copy import deepcopy


class Donut:

    def __init__(self, filename: str):
        self.grid = {}                  # Key=(x, y), Value=character at that coordinate.

        self.width, self.height = 0, 0  # Dimensions of the grid.

        self.portals = {}               # Key is entrance to portal (x, y), value is exit from portal (x, y).

        self.start = (0, 0)             # Coordinates of 'AA'.
        self.end = (0, 0)               # Coordinates of 'ZZ'.

        self.shortest_to_square = {}    # Least steps found to this square. Key=(x, y), Value=steps.

        self.best = 0                   # Shortest route from AA to ZZ found so fae.

        f = open(filename)
        whole_text = (f.read())

        x, y = 0, 0
        for each_char in whole_text:
            if each_char == '\n':           # New-line.
                x = 0
                y += 1
            else:
                self.grid[x, y] = each_char
                x += 1

                if x > self.width:
                    self.width = x
        self.height = y + 1
        f.close()

    @staticmethod
    def is_cap_letter(test_char: str):
        """Return true if the parm character is a capital letter."""
        if 'A' <= test_char <= 'Z':
            return True
        return False

    def is_special(self, cap_1: str, cap_2: str, dot: str) -> bool:
        """If the first two parms are capital letters, and the third is a dot, then return True.
        Example sequence is 'BC.'"""

        if self.is_cap_letter(cap_1) and self.is_cap_letter(cap_2) and dot == '.':
            return True
        return False

    def find_special_squares(self) -> {}:
        """Return a dictionary of special square information. Key=(x, y), Value=Name of special square."""
        found = {}

        for x in range(self.width):
            for y in range(self.height):

                if x < self.width - 2:
                    one = self.grid[x, y]
                    two = self.grid[x + 1, y]
                    three = self.grid[x + 2, y]

                    # "BC."
                    if self.is_special(cap_1=one, cap_2=two, dot=three):
                        found[x + 2, y] = one + two

                    # ".BC"
                    if self.is_special(cap_1=two, cap_2=three, dot=one):
                        found[x, y] = two + three

                if y < self.height - 2:
                    one = self.grid[x, y]
                    two = self.grid[x, y + 1]
                    three = self.grid[x, y + 2]

                    # B
                    # C
                    # .
                    if self.is_special(cap_1=one, cap_2=two, dot=three):
                        found[x, y + 2] = one + two

                    # .
                    # B
                    # C
                    if self.is_special(cap_1=two, cap_2=three, dot=one):
                        found[x, y] = two + three

        return found

    def set_specials(self):
        """Set the attributes of Start, end End
        Also set attributes of Portals."""
        specials = self.find_special_squares()

        for vertex in specials:
            name = specials[vertex]

            if name == 'AA':                    # "Every maze on Pluto has a start (the open tile next to AA)..."
                self.start = vertex
            elif name == 'ZZ':                  # "... and an end (the open tile next to ZZ)"
                self.end = vertex

            else:                               # The start and end specials are not real portals.
                for pair in specials:
                    if specials[pair] == name and vertex != pair:
                        self.portals[vertex] = pair

    def search(self,
               current_square: (int, int),      # Start / continue search from here.
               squares_visited: []):            # List of squares previously visited.
        """Do a recursive search of squares, until end (ZZ) is found."""

        one_way_only = True

        while one_way_only:
            steps_taken = len(squares_visited)

            # Check if we've made it to the end of the maze.
            if current_square == self.end:
                # No previous best, so this must be the best found so far...
                # ... or better than previous best.
                if self.best == 0 or steps_taken < self.best:
                    self.best = steps_taken
                    print('Best so far:', self.best)
                return

            # Is this a good route to whatever the current square is?
            if current_square not in self.shortest_to_square:  # If never been to this square before, then this is best.
                self.shortest_to_square[current_square] = steps_taken
            else:
                # If improvement on previous best route to this then record this.
                if steps_taken < self.shortest_to_square[current_square]:
                    self.shortest_to_square[current_square] = steps_taken
                else:  # No improvement on previous route to this square, so give up.
                    return

            possible_next_squares = []

            # If standing next to portal, we could go through it...
            if current_square in self.portals:
                if self.portals[current_square] not in squares_visited:     # ... unless it is a backtrack.
                    possible_next_squares.append(self.portals[current_square])

            (curr_x, curr_y) = current_square

            # Look for a '.' adjacent to the current square.
            for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                possible = (curr_x + dx, curr_y + dy)

                # If the possible is a '.', and we haven't been to it before in this search, then OK.
                if self.grid[possible] == '.' and possible not in squares_visited:
                    possible_next_squares.append(possible)

            if len(possible_next_squares) == 0:             # Dead end, so give up.
                return

            elif len(possible_next_squares) == 1:           # Only one possible square to go to next, so iterate.
                current_square = possible_next_squares[0]
                squares_visited.append(current_square)

            else:                                           # Several possible next squares, so recurse.
                for possible in possible_next_squares:
                    new_squares_visited = deepcopy(squares_visited)
                    new_squares_visited.append(possible)
                    self.search(current_square=possible, squares_visited=new_squares_visited)
                one_way_only = False                        # Stop iterative loop.


this_donut = Donut('input.txt')
this_donut.set_specials()

this_donut.search(current_square=this_donut.start, squares_visited=[])
print('Part 1:', this_donut.best)
