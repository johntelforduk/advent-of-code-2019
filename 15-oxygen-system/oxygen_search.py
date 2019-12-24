# Part of solution to day 15 of AOC 2019, "Oxygen System".
# https://adventofcode.com/2019/day/15


from intcode_computer import dict_computer as comp
from copy import deepcopy


class Droid:

    def __init__(self):

        self.curr_x, self.curr_y = 0, 0                             # Current coordinates of the droid in the world.

        # Master comp is the machine 'image' that the work comp will be copied from.
        self.master_comp = comp.Computer(output_to_screen=False)
        self.master_comp.load_file('input.txt')

        self.comp = deepcopy(self.master_comp)

    def reset_droid(self):
        """Reset the droid, position back at origin, with a freshly reset computer."""
        self.curr_x = 0
        self.curr_y = 0
        self.comp = deepcopy(self.master_comp)


class World:

    def __init__(self):

        # Key=(x, y), Value=what was found at that square.
        # Values are 0 for wall, 1 for explorable space, 2 for oxygen system.
        self.grid = {(0, 0): 1}

        self.paths = {(0, 0): []}                               # The path the droid should follow to get to a place.
        self.unexplored = {(0, 0): [1, 2, 3, 4]}                # Key is a square, Value=Direction not yet explored,

        self.oxygen_system = (0, 0)

    def print(self, include_droid: bool):
        """Print out the map. Show the droid's starting position as 'D', and the Oxygen system as 'O'."""
        min_y, max_y, min_x, max_x = 0, 0, 0, 0

        # Find the edges of the grid.
        for (x, y) in self.grid:
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        # Print the world map to stdout.
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                vertex = (x, y)
                if vertex == (0, 0) and include_droid:          # Origin is printed as 'D'.
                    cell = 'D'
                elif vertex in self.grid:
                    cell = {0: '#', 1: '.', 2: 'O'}[self.grid[vertex]]
                else:
                    cell = '#'                                  # Any undiscovered cells are unreachable.
                print(cell, end='')
            print()

    def save(self, filename: str):
        """Save the world map to parm filename."""
        f = open(filename, 'w')

        # Write the location of the oxygen tank - x,y
        (ox_x, ox_y) = self.oxygen_system
        f.write(str(ox_x) + ',' + str(ox_y))

        # Write the contents of each grid location - x,y,contents
        for location in self.grid:
            (loc_x, loc_y) = location
            contents = self.grid[location]
            f.write('\n' + str(loc_x) + ',' + str(loc_y) + ',' + str(contents))
        f.close()

    def load(self, filename: str):
        """Load the world map from parm filename."""
        f = open(filename, 'r')
        whole_text = f.read()

        line_one = True
        for each_line in whole_text.split('\n'):
            if line_one:
                [ox_x, ox_y] = each_line.split(',')
                self.oxygen_system = (int(ox_x), int(ox_y))
                line_one = False
            else:
                [loc_x, loc_y, contents] = each_line.split(',')
                self.grid[(int(loc_x), int(loc_y))] = int(contents)
        f.close()


class Search:

    def __init__(self):
        self.world = World()
        self.droid = Droid()

    def take_a_step(self, direction: int):
        """Move the droid one step in parm direction. Return the output from the computer."""
        assert direction in {1, 2, 3, 4}
        self.droid.comp.input = direction
        self.droid.comp.run_until_output()
        output = self.droid.comp.output

        # Move the droid.
        self.droid.curr_x += {1: 0, 2: 0, 3: -1, 4: 1}[direction]
        self.droid.curr_y += {1: -1, 2: 1, 3: 0, 4: 0}[direction]

        return output

    def go_to_place(self, place: (int, int)):
        """Move the droid to the parm place."""
        self.droid.reset_droid()                        # Reset the droid to origin. Reset it's computer too.
        path_to_place = self.world.paths[place]

        if path_to_place is []:
            return

        for step in path_to_place:
            output = self.take_a_step(step)
            assert output != 0                          # Replaying existing path should always be successful moves.

    def explore(self):
        """Explore the world, looking for the oxygen system."""
        search_unexplored = deepcopy(self.world.unexplored)

        for place in search_unexplored:
            for direction in search_unexplored[place]:
                # This is a direction that hasn't been tried yet for this place.

                self.go_to_place(place)

                # Now try to take the step.
                output = self.take_a_step(direction)

                new_place = (self.droid.curr_x, self.droid.curr_y)

                # If we moved, then update the map with whatever we found.
                if output == 0:             # 0 is hit a wall, so map that.
                    self.world.grid[new_place] = output

                else:                       # We didn't hit a wall!
                    # If its the first time we've been here, add it to the grid, and record the path to it.
                    if new_place not in self.world.grid:
                        self.world.grid[new_place] = output

                        if output == 2:     # 2 = Oxygen system.
                            self.world.oxygen_system = new_place

                        path_to_new_place = deepcopy(self.world.paths[place])
                        path_to_new_place.append(direction)
                        self.world.paths[new_place] = path_to_new_place
                        self.world.unexplored[new_place] = [1, 2, 3, 4]

            # This square has been explored so remove it from dictionary of unexplored places.
            del self.world.unexplored[place]
