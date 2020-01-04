# Part of solution to day 20 of AOC 2019, "Donut Maze".
# https://adventofcode.com/2019/day/20


class Donut:

    def __init__(self, filename: str):
        self.grid = {}          # Key=(x, y), Value=character at that coordinate.

        self.width, self.height = 0, 0  # Dimenensions of the grid.

        # portals_0 for level 0, and portals_n for all other levels.
        # Key is entrance to portal (x, y), value is exit from portal (x, y, level_delta).
        # level_delta is one of 1 (go deeper), -1 (go higher).
        self.portals_0 = {}
        self.portals_n = {}

        self.start = (0, 0)             # Coordinates of 'AA'.
        self.end = (0, 0)               # Coordinates of 'ZZ'.

        self.shortest_to_square = {}    # Least steps found to this square. Key=(x, y, level), Value=steps.

        self.shortest_v_to_v = {}       # Shortest distance from vertex to vertex on same level.

        self.max_depth = 0              # Limit for map levels to search.

        self.best = 0                   # Shortest route from AA to ZZ found so far.

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
        """Return a dictionary of special square information. Key=(x, y, position), Value=Name of special square.
        Position is one of 'Outer', 'Inner'."""

        found = {}

        for x in range(self.width):
            for y in range(self.height):

                if x < self.width - 2:
                    one = self.grid[x, y]
                    two = self.grid[x + 1, y]
                    three = self.grid[x + 2, y]

                    # "BC."
                    if self.is_special(cap_1=one, cap_2=two, dot=three):
                        if x == 0:
                            found[x + 2, y, 'Outer'] = one + two
                        else:
                            found[x + 2, y, 'Inner'] = one + two

                    # ".BC"
                    if self.is_special(cap_1=two, cap_2=three, dot=one):
                        if x == self.width - 3:
                            found[x, y, 'Outer'] = two + three
                        else:
                            found[x, y, 'Inner'] = two + three

                if y < self.height - 2:
                    one = self.grid[x, y]
                    two = self.grid[x, y + 1]
                    three = self.grid[x, y + 2]

                    # B
                    # C
                    # .
                    if self.is_special(cap_1=one, cap_2=two, dot=three):
                        if y == 0:
                            found[x, y + 2, 'Outer'] = one + two
                        else:
                            found[x, y + 2, 'Inner'] = one + two

                    # .
                    # B
                    # C
                    if self.is_special(cap_1=two, cap_2=three, dot=one):
                        if y == self.height - 3:
                            found[x, y, 'Outer'] = two + three
                        else:
                            found[x, y, 'Inner'] = two + three

        return found

    def set_specials(self):
        """Set the attributes of Start, end End
        Also set attributes of Portals."""
        specials = self.find_special_squares()

        for (from_x, from_y, from_position) in specials:
            from_name = specials[(from_x, from_y, from_position)]

            if from_name == 'AA':                   # "Every maze on Pluto has a start (the open tile next to AA)..."
                self.start = (from_x, from_y, 0)    # (x, y, level)
            elif from_name == 'ZZ':                 # "... and an end (the open tile next to ZZ)"
                self.end = (from_x, from_y, 0)      # (x, y, level)

            else:                                   # The start and end specials are not real portals.
                if from_position == 'Inner':
                    opposite_position = 'Outer'
                else:
                    opposite_position = 'Inner'

                for (to_x, to_y, to_position) in specials:
                    to_name = specials[(to_x, to_y, to_position)]

                    # "When you enter the maze, you are at the outermost level; when at the outermost level, only the
                    # outer labels AA and ZZ function (as the start and end, respectively); all other outer labeled
                    # tiles are effectively walls. At any other level, AA and ZZ count as walls, but the other outer
                    # labeled tiles bring you one level outward."

                    if from_name == to_name and to_position == opposite_position:
                        if from_position == 'Outer':
                            self.portals_n[(from_x, from_y)] = (to_x, to_y, -1)
                        else:
                            self.portals_0[(from_x, from_y)] = (to_x, to_y, 1)
                            self.portals_n[(from_x, from_y)] = (to_x, to_y, 1)

    def search_shortest_v_to_v(self, from_v: (int, int), waypoint: (int, int), to_v: (int, int), squares_visited: []):
        """Find shortest route between parm pair of vertices on same level.
        Continue search from parm waypoint."""

        one_way_only = True

        while one_way_only:
            steps_taken = len(squares_visited)

            # Check if we've made it to target square.
            if waypoint == to_v:
                # No previous best, so this must be the best found so far...
                if (from_v, to_v) not in self.shortest_v_to_v:
                    self.shortest_v_to_v[(from_v, to_v)] = steps_taken
                # ... or better than previous best.
                elif steps_taken < self.shortest_v_to_v[(from_v, to_v)]:
                    self.shortest_v_to_v[(from_v, to_v)] = steps_taken
                return

            possible_next_squares = []

            (curr_x, curr_y) = waypoint

            # Look for a '.' adjacent to the current square.
            for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

                possible = (curr_x + dx, curr_y + dy)

                # If the possible is a '.', and we haven't been to it before in this search, then OK.
                if self.grid[possible] == '.' and possible not in squares_visited:
                    possible_next_squares.append(possible)

            if len(possible_next_squares) == 0:             # Dead end, so give up.
                return

            elif len(possible_next_squares) == 1:           # Only one possible square to go to next, so iterate.
                waypoint = possible_next_squares[0]
                squares_visited.append(waypoint)

            else:                                           # Several possible next squares, so recurse.
                for possible in possible_next_squares:
                    # new_squares_visited = deepcopy(squares_visited)
                    new_squares_visited = []
                    for x in squares_visited:
                        new_squares_visited.append(x)

                    new_squares_visited.append(possible)

                    self.search_shortest_v_to_v(from_v=from_v,
                                                waypoint=possible,
                                                to_v=to_v,
                                                squares_visited=new_squares_visited)
                one_way_only = False                        # Stop iterative loop.

    def set_shortest_v_to_v(self):
        """Find shortest routes from each vertex to each other vertex on same level, without using portals."""
        specials = self.find_special_squares()

        for from_special in specials:
            for to_special in specials:
                if from_special != to_special:                  # No need for route from vertex to itself.
                    (from_x, from_y, _) = from_special
                    (to_x, to_y, _) = to_special

                    self.search_shortest_v_to_v(from_v=(from_x, from_y),
                                                waypoint=(from_x, from_y),
                                                to_v=(to_x, to_y),
                                                squares_visited=[])

    def search(self,
               current_square: (int, int, int),     # (x, y, level). Start / continue search from here.
               squares_visited: [],                 # List of significant squares already visited, each (x, y, level).
               steps_taken: int):                   # Number of steps taken.
        """Do a recursive search of squares, until end (ZZ) is found."""

        one_way_only = True

        while one_way_only:
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

            possible_next_squares = {}

            (curr_x, curr_y, curr_level) = current_square
            curr_cartesian = (curr_x, curr_y)       # Current square in (x, y) plane only (no level axis).

            # If recursive search is going to deep, give up.
            if curr_level > self.max_depth:
                return

            # If standing next to portal, we could go through it...
            portal_exit = ()                                                    # Assume we won't go through a portal.
            if curr_level == 0:
                if curr_cartesian in self.portals_0:
                    portal_exit = self.portals_0[curr_cartesian]

            else:                   # Current level is not 0.
                if curr_cartesian in self.portals_n:
                    (exit_x, exit_y, level_delta) = self.portals_n[curr_cartesian]
                    portal_exit = (exit_x, exit_y, curr_level + level_delta)

            if portal_exit is not () and portal_exit not in squares_visited:    # ... unless it is a backtrack.
                possible_next_squares[portal_exit] = 1                          # Going through the portal is 1 step.

            # Consider all possible shortest routes from current square to special squares on same level.
            for (route_from, route_to) in self.shortest_v_to_v:
                (route_to_x, route_to_y) = route_to
                route_to_3d = (route_to_x, route_to_y, curr_level)
                if curr_cartesian == route_from and route_to_3d not in squares_visited:
                    possible_next_squares[route_to_x,
                                          route_to_y,
                                          curr_level] = self.shortest_v_to_v[route_from, route_to]

            if len(possible_next_squares) == 0:             # Dead end, so give up.
                return

            elif len(possible_next_squares) == 1:           # Only one possible square to go to next, so iterate.
                for the_one in possible_next_squares:
                    current_square = the_one
                squares_visited.append(current_square)
                steps_taken += possible_next_squares[current_square]

            else:                                           # Several possible next squares, so recurse.
                for possible in possible_next_squares:
                    # Make a copy of the squares_visited list.
                    new_squares_visited = []
                    for x in squares_visited:
                        new_squares_visited.append(x)

                    new_squares_visited.append(possible)
                    new_steps_taken = steps_taken + possible_next_squares[possible]

                    self.search(current_square=possible,
                                squares_visited=new_squares_visited,
                                steps_taken=new_steps_taken)
                one_way_only = False                        # Stop iterative loop.


this_donut = Donut('input.txt')
this_donut.set_specials()

this_donut.max_depth = int(len(this_donut.portals_n) / 2)

this_donut.set_shortest_v_to_v()

this_donut.search(current_square=this_donut.start, squares_visited=[], steps_taken=0)
print('Part 2:', this_donut.best)
