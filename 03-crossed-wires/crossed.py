# Solution to day 3 of AOC 2019, "Crossed Wires".
# https://adventofcode.com/2019/day/3


def dist_from_origin(vertex) -> int:
    """Return the Manhattan distance that the parm vertex is from (0, 0)."""
    (x, y) = vertex
    return abs(x) + abs(y)


def path_to_vertices(route: str) -> (set, dict):
    """Returns a pair of items. First item is a set of vertices visited for a parm route string.
    Each vertex is a tuple (x, y). Origin vertex is omitted.
    Second item is a dictionary of number of steps to first reach each vertex."""

    vertices = set()                                # The set of vertices that will be returned.

    # Dictionary of distances that will be returned. Key is (x, Y), value is steps taken to first get there.
    vertex_distances = {}

    x, y = 0, 0                                     # Origin of the journey the wire will take.
    total_steps = 0                                 # Steps taken to get to the vertex.

    for instruction in route.split(','):            # Instructions are comma delimited.

        # Example of a step, 'U414'...
        direction = instruction[0]                  # direction = 'U'
        distance = int(instruction[1:])             # distance = 414

        assert direction in {'U', 'R', 'D', 'L'}    # Must be 'U'p, 'R'ight, 'D'own or 'L'eft.
        if direction == 'U':
            dx, dy = 0, -1                          # Set deltas according to the directions.
        elif direction == 'R':
            dx, dy = 1, 0
        elif direction == 'D':
            dx, dy = 0, 1
        else:
            dx, dy = -1, 0

        for step in range(distance):                # Take the 'distance' number of steps.
            x += dx
            y += dy
            vertex = (x, y)
            vertices.add(vertex)

            total_steps += 1
            if vertex not in vertex_distances:      # Only want the shortest distance to the vertex in the dictionary.
                vertex_distances[vertex] = total_steps

    return vertices, vertex_distances


f = open('input.txt')
whole_text = (f.read())
string_list = whole_text.split()                     # Split string by whitespace.

wire_1 = string_list[0]
wire_2 = string_list[1]

(vertices_1, vertex_distances_1) = path_to_vertices(wire_1)
(vertices_2, vertex_distances_2) = path_to_vertices(wire_2)

crossed_wires = vertices_1.intersection(vertices_2)     # Wires cross where vertices intersect.

distances = list(map(dist_from_origin, crossed_wires))  # Calculate Manhattan distance for each crossed wire vertex.
distances.sort()                                        # Put the shortest distance in position [0] of the list.

print('Part 1:', distances[0])

fewest_steps_found = None
for crossed in crossed_wires:
    combined_steps = vertex_distances_1[crossed] + vertex_distances_2[crossed]
    if fewest_steps_found is None or combined_steps < fewest_steps_found:
        fewest_steps_found = combined_steps

print('Part 2:', fewest_steps_found)
