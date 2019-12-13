# Solution to part 1 of day 10 of AOC 2019, "Monitoring Station".
# https://adventofcode.com/2019/day/10

# This is an integer solution. Looking at the AOC sub-reddit, it seem that most solutions use trigonometry.


# TODO Figure out why test_1.txt returns 7. It should return 8.


from math import gcd                    # Greatest common divisor.


def num_to_one(x: int) -> int:
    """Returns +1 or -1, depending on whether parm is +ve or -ve."""
    if x < 0:
        return -1
    else:
        return 1


def check(origin: (int, int), delta: (int, int)):
    """Fine out if the asteroid at vertex ORIGIN can see the asteroid at vertex ORIGIN + DELTA."""
    global count_seeable
    global un_seeable
    global asteroid_map

    (origin_x, origin_y) = origin
    (dx, dy) = delta

    check_vertex = (origin_x + dx, origin_y + dy)

    if check_vertex in asteroid_map and check_vertex not in un_seeable:
        count_seeable += 1

        divisor = gcd(dx, dy)               # Makes unsseable be added with smallest possible integer steps.
        small_dx = dx // divisor
        small_dy = dy // divisor

        # Mark as unseeable asteroids in line away from origin, in delta direction.
        for i in range(view_horizon):

            if dy == 0:                                                 # Vertical line.
                un_seeable_x = origin_x + dx + i * num_to_one(dx)
                un_seeable_y = origin_y

            elif dx == 0:                                               # Horizontal line.
                un_seeable_y = origin_y + dy + i * num_to_one(dy)
                un_seeable_x = origin_x

            elif abs(dx) == abs(dy):                                    # Diagonal line.
                un_seeable_x = origin_x + dx + i * num_to_one(dx)
                un_seeable_y = origin_y + dy + i * num_to_one(dy)
            else:
                un_seeable_x = origin_x + i * small_dx
                un_seeable_y = origin_y + i * small_dy

            un_seeable.add((un_seeable_x, un_seeable_y))


def search(origin: (int, int), max_radius: int):
    """Search outwards looking for visible asteroids."""

    for radius in range(1, max_radius):

        for i in range(1 + radius * 2):
            check(origin, delta=(i - radius, - radius))         # Upper horizontal line.
            check(origin, delta=(i - radius, radius))           # Lower horizontal line.
            check(origin, delta=(- radius, i - radius))         # Left vertical line.
            check(origin, delta=(radius, i - radius))           # Right vertical line.


f = open('input.txt')
whole_text = (f.read())

width, height = 0, 0                    # Dimensions of the asteroid map.
asteroid_map = {}                       # Key is vertex tuple (x, y), value is '.' or '#'.
view_horizon = max(width, height) + 5   # How far to look for asteroids.

x, y = 0, 0
for this_char in whole_text:
    if y > height:
        height = y
    if this_char == '\n':               # Start of a new line.
        x = 0
        y += 1
    else:
        if this_char == '#':
            asteroid_map[(x, y)] = this_char
        if x > width:                   # New maximum width found.
            width = x
        x += 1

f.close()

view_horizon = max(width, height) + 5   # How far to look for asteroids.

best, best_x, best_y = 0, 0, 0

for test_x in range(width):
    for test_y in range(height):
        count_seeable = 0
        un_seeable = set()              # Set of unseeable vertices. Initialised to empty set.

        if (test_x, test_y) in asteroid_map:
            search(origin=(test_x, test_y), max_radius=view_horizon)

            if count_seeable > best:
                best = count_seeable
                best_x = test_x
                best_y = test_y

print('Part 1:', best, best_x, best_y)
