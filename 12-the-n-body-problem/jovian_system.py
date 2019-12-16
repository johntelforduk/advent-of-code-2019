# Part of solution to day 12 of AOC 2019, "The N-Body Problem".
# https://adventofcode.com/2019/day/12

from math import gcd
from functools import reduce


def lcm(a, b):
    return a*b // gcd(a, b)


def get_lcm_for(your_list):
    return reduce(lambda x, y: lcm(x, y), your_list)


class JovianSystem:

    def __init__(self):
        self.num_axis = 3               # This system is defined in terms of 3-dimensional space (x, y, z).

        # List of moon position. Each element is a moon element.
        # Each moon element is a list representing the coordinates of the moon [x, y, z].

        self.pos = []

        # List of moon velocities. Each element is a moon velocity.
        # Each velocity element is a list representing the velocity of the moon [dx, dy, dz].
        self.vel = []

        self.steps = 0                  # Number of iterations of system simulated so far.
        self.num_moons = 0              # Number of moons in the system.

    def load_file(self, filename: str):
        """Load parm file of starting position data into position list. Also create list of starting velocities,
        which initialises to all zeros."""
        f = open(filename)
        whole_text = (f.read())
        moon_list = whole_text.split('\n')  # Split string by newline.

        for moon in moon_list:
            positions = (moon.lstrip('<').rstrip('>')).split(',')           # Strip off leading and trailing chevrons.
            position_list = []
            for each_position in positions:
                parsed_position = int(each_position.lstrip(' ')[2:])        # Strip of leading spaces.
                position_list.append(parsed_position)
            self.pos.append(position_list)
            self.vel.append([0, 0, 0])
        self.num_moons = len(self.pos)

    def axis_num_to_name(self, axis_num: int) -> str:
        """For parm number, return the axis letter that corresponds with it."""
        return {0: 'x', 1: 'y', 2: 'z'}[axis_num]

    def print(self):
        """Print out current status of the system."""
        print('After', self.steps, 'steps:')

        for moon in range(self.num_moons):
            print('pos=<', end='')
            for axis in range(self.num_axis):
                if axis != 2:
                    ending = ', '
                else:
                    ending = '>, vel=<'
                print(self.axis_num_to_name(axis), '=', self.pos[moon][axis], end=ending)
            for axis in range(self.num_axis):
                if axis != 2:
                    ending = ', '
                else:
                    ending = '>'
                print(self.axis_num_to_name(axis), '=', self.vel[moon][axis], end=ending)
            print()
        print()

    def time_step(self):
        """Calculate new velocities of each moon. Calculate new positions of each moon."""

        # Calculate velocities.
        for this_moon in range(self.num_moons):
            for compare_moon in range(self.num_moons):
                if this_moon != compare_moon:                   # Don't compare a moon with itself.
                    for axis in range(self.num_axis):
                        if self.pos[this_moon][axis] < self.pos[compare_moon][axis]:
                            self.vel[this_moon][axis] += 1
                        elif self.pos[this_moon][axis] > self.pos[compare_moon][axis]:
                            self.vel[this_moon][axis] -= 1

        # Calculate positions by applying velocities.
        for this_moon in range(self.num_moons):
            for axis in range(self.num_axis):
                self.pos[this_moon][axis] += self.vel[this_moon][axis]

        self.steps += 1

    def print_energy(self):
        """Calculate total energy, and print it to screen."""
        total_energy = 0

        for moon in range(self.num_moons):
            pot = 0
            kin = 0

            for axis in range(self.num_axis):
                pot += abs(self.pos[moon][axis])
                kin += abs(self.vel[moon][axis])

            # print (pot, kin)
            total_energy += pot * kin
        print('Part 1:', total_energy)

    def snapshot_axis(self, axis: int) -> [int]:
        """For parm axis number, return a list which is current positions and velocities of all moons on that axis."""
        axis_values = []

        for moon in self.pos:
            axis_values.append(moon[axis])
        for moon in self.vel:
            axis_values.append(moon[axis])

        return axis_values

    def find_matches(self):
        """Predict when universe will return to its original state."""
        start_values = []
        for axis in range(self.num_axis):
            start_values.append(self.snapshot_axis(axis))

        cadences = {}

        while len(cadences) < self.num_axis:        # Keep searching until a cadence for each axis has been found.

            self.time_step()                        # Move time on one tick.

            for axis in range(self.num_axis):

                # We want lowest cadence, so skip test if cadence already found for this axis.
                if axis not in cadences:
                    this_snapshot = self.snapshot_axis(axis)

                    if start_values[axis] == this_snapshot:     # For this axis, positions and velocities match start.
                        cadences[axis] = self.steps

        # Convert the values of the cadences dict into a list.
        cadence_list = []
        for c in cadences:
            cadence_list.append(cadences[c])

        best = get_lcm_for(cadence_list)
        print('Part 2:', best)
