# Part of solution to part 2 of day 10 of AOC 2019, "Monitoring Station".
# https://adventofcode.com/2019/day/10

import math


def translation(vertex: (int, int), delta: (int, int)) -> (int, int):
    """Move a vertex in 2d space."""
    (vertex_x, vertex_y) = vertex
    (delta_x, delta_y) = delta                          # Delta is the amount to move the vertex by.
    return vertex_x + delta_x, vertex_y + delta_y


# For explanation of the maths, see,
# https://en.wikipedia.org/wiki/Rotation_of_axes#Derivation
def rotation(vertex: (int, int), rotation_radians: float) -> (int, int):
    """Rotate the parm vertex around the origin (0, 0) by parm parm radians."""
    (vertex_x, vertex_y) = vertex

    return (round(vertex_x * math.cos(rotation_radians) + vertex_y * math.sin(rotation_radians)),
            round(- vertex_x * math.sin(rotation_radians) + vertex_y * math.cos(rotation_radians)))


def angle_from_origin(vertex: (int, int)) -> float:
    """Returns the angle from origin to parm vertex. North is 0, East is pi / 2."""
    (x, y) = vertex

    # First deal with due N, S, E, W.
    if x == 0 and y >= 0:                           # North
        return 0
    elif x == 0 and y < 0:                          # South
        return math.pi
    elif y == 0 and x > 0:                          # East.
        return math.pi / 2
    elif y == 0 and x < 0:                          # West.
        return 3 * math.pi / 2

    twist = 0

    # Keep rotating 90 degrees anti-clockwise until vertex is in top right quadrant.
    while x < 0 or y < 0:
        (x, y) = rotation((x, y), -math.pi / 2)     # Rotate 90 degrees anti-clockwise
        twist += math.pi / 2

    return twist + math.atan(x / y)


def angle(v1: (int, int), v2: (int, int)) -> float:
    """Returns the angle in radians between the two parm vertices. North is 0, East is pi / 2."""

    # Imagine both vertices being move, so that 1st one is on the origin.
    (v1_x, v1_y) = v1
    v2_moved = translation(v2, (-v1_x, -v1_y))

    # Now the angle between the 2 vertices is the angle between the origin and the 2ns vertex.
    return angle_from_origin(vertex=v2_moved)


def distance(v1: (int, int), v2: (int, int)) -> float:
    """Returns the distance between two vertices."""
    (v1_x, v1_y) = v1
    (v2_x, v2_y) = v2
    return math.sqrt((v1_x - v2_x) ** 2 + (v1_y - v2_y) ** 2)     # Pythagoras theorem.


class AsteroidField:

    def __init__(self, filename: str):

        self.asteroid_map = {}                      # Key is vertex tuple (x, y), value is '.' or '#'.
        self.width, self.height = 0, 0              # Dimensions of the asteroid map.
        self.station = (0, 0)                       # Vertex where the Monitoring Station is located.

        self.targets = []                           # List of laser targets. Asteroids are removed from it when shot.
        self.shot_order = []                        # List of asteroids in the order they were shot.

        f = open(filename)
        whole_text = (f.read())

        x, y = 0, 0
        for this_char in whole_text:
            if y > self.height:
                self.height = y
            if this_char == '\n':                   # Start of a new line.
                x = 0
                y += 1
            else:
                if this_char == '#':
                    self.asteroid_map[(x, y)] = this_char
                if x > self.width:                  # New maximum width found.
                    self.width = x
                x += 1

        f.close()

    def flip(self, vertex: (int, int)) -> (int, int):
        """Turn conventional co-ordinates, where origin is bottom-left, to the system used in this puzzles where origin
        is at top left. For example,

        (0, 0)  (1, 0)   (2, 0)
        (0, 1)  (1, 1)   (2, 1)
        (0, 2)  (1, 2)   (2, 2)"""

        (x, y) = vertex
        return x, self.height - y

    def flip_all(self):
        """Do coordinate flipping for all asteroids in the field, as well as the station."""
        old_asteroid_map = self.asteroid_map.copy()

        self.asteroid_map = []

        for asteroid in old_asteroid_map:
            self.asteroid_map.append(self.flip(asteroid))

        self.station = self.flip(self.station)              # Flip station coordinates.

    def find_targets(self):
        """Make list of targets. Each item in list is list of [angle, distance, (x, y)]"""
        for asteroid in self.asteroid_map:
            self.targets.append([angle(self.station, asteroid),
                                distance(self.station, asteroid),
                                asteroid])

    def shoot_targets(self):
        """Make list of targets sorted into order they should be shot in."""

        while len(self.targets) != len(self.shot_order):
            last_angle_shot = None

            for asteroid in self.targets:
                [this_angle, _, vertex] = asteroid
                if this_angle != last_angle_shot and self.flip(vertex) not in self.shot_order:
                    self.shot_order.append(self.flip(vertex))
                    last_angle_shot = this_angle
