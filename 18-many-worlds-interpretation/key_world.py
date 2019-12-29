# Part of solution to day 18 of AOC 2019, "Many-Worlds Interpretation".
# https://adventofcode.com/2019/day/18


from copy import deepcopy


class KeyWorld:

    def is_door(self, test_vertex: (int, int)) -> bool:
        """Return True, if the parm vertex is a door."""
        if 'A' <= self.grid[test_vertex] <= 'Z':
            return True
        return False

    def is_key(self, test_vertex: (int, int)) -> bool:
        """Return True, if the parm vertex is a key."""
        if 'a' <= self.grid[test_vertex] <= 'z':
            return True
        return False

    @staticmethod
    def door_to_key(door: str) -> str:
        """Return the key needed to open parm door."""
        return chr(ord(door) + 32)          # For example, door "A" needs key "a".

    def __init__(self, filename: str):
        self.grid = {}                      # Key=vertex (x, y), Value=character at that vertex.

        self.entrance = (0, 0)              # Position of the entrance, '@'.
        self.keys = {}                      # Key=key letter, eg 'a', Value=cordinates of the key.
        self.num_keys = 0                   # Count of the number of keys in the world.

        self.shortest_leg = {}              # Key=(From, To) eg 'Origin', 'a', etc., Value=(Required Keys, Steps)
        self.origin_to_waypoint = {}        # Key=(origin, dest, waypoint), Value=number of steps

        self.shortest = {}                  # Key=(origin, dest_vertex, sorted_keys), Value=steps taken.

        self.shortest_route_steps = 0       # Shortest route found that collects all of the keys.

        f = open(filename, 'r')
        whole_text = f.read()

        x, y = 0, 0
        for this_char in whole_text:
            if this_char == '\n':           # Start a new line.
                x = 0
                y += 1
            else:
                self.grid[x, y] = this_char

                if this_char == '@':        # '@' is the entrance.
                    self.entrance = (x, y)

                if self.is_key(test_vertex=(x, y)):
                    self.keys[this_char] = (x, y)
                    self.num_keys += 1
                x += 1
        f.close()

    def find_shortest_route(self,
                            origin: (int, int),
                            dest: (int, int),
                            waypoint: (int, int),
                            vertices_visited: [],
                            required_keys: str):
        """Find shortest route from parm waypoint to parm destination. Store this route in shortest_leg attribute."""

        (x, y) = waypoint
        num_steps = len(vertices_visited)

        # Is this the shortest distance found so far from origin to waypoint?
        if (origin, dest, waypoint) not in self.origin_to_waypoint:   # Nothing recorded for this o -? w, so must be best.
            self.origin_to_waypoint[(origin, dest, waypoint)] = num_steps
        else:
            best = self.origin_to_waypoint[(origin, dest, waypoint)]
            if num_steps < best:
                self.origin_to_waypoint[(origin, dest, waypoint)] = num_steps
            else:
                return

        iterating = True

        while iterating:
            new_vertices = []                       # All vertices to try.

            for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_vertex = (x + dx, y + dy)

                # Can't move to the vertex if it's a wall.
                # And should not double back on self.
                if self.grid[new_vertex] != '#' and new_vertex not in vertices_visited:
                    new_vertices.append(new_vertex)

            if len(new_vertices) == 1:      # Only one possible new vertex to try, so keep iterating.

                new_vertex = new_vertices[0]    # There is only new vertex in this list, at index 0.

                # Add this vertex to the vertices visited.
                # new_vertices_visited = deepcopy(vertices_visited)
                vertices_visited.append(new_vertex)

                # If the new vertex is door, then record that we need a key to go through it.
                # new_keys = required_keys
                if self.is_door(test_vertex=new_vertex):
                    required_keys = required_keys + self.door_to_key(self.grid[new_vertex])

                num_steps = len(vertices_visited)

                # If already taken more steps than best route found for this pair of vertices, then give up.
                if (origin, dest) in self.shortest_leg:
                    (_, best_num_steps) = self.shortest_leg[(origin, dest)]
                    if best_num_steps < num_steps:
                        return

                # We found the destination!
                if new_vertex == dest:
                    if (origin, dest) not in self.shortest_leg:  # First route found, so add to dictionary.
                        self.shortest_leg[(origin, dest)] = (required_keys, num_steps)
                    else:
                        # (_, best_num_steps) = self.shortest_leg[(origin, dest)]
                        if num_steps < best_num_steps:  # If better than previous best, store it.
                            self.shortest_leg[(origin, dest)] = (required_keys, num_steps)

                    # Route found, so stop searching.
                    return

                (x, y) = new_vertex

            elif len(new_vertices) > 1:         # More than 1 new vertex to try, so try them recursively.
                iterating = False               # STOP iterating (start recursing).
                for new_vertex in new_vertices:

                    # Add this vertex to the vertices visited.
                    new_vertices_visited = deepcopy(vertices_visited)
                    new_vertices_visited.append(new_vertex)

                    # If the new vertex is door, then record that we need a key to go through it.
                    new_keys = required_keys
                    if self.is_door(test_vertex=new_vertex):
                        new_keys = new_keys + self.door_to_key(self.grid[new_vertex])

                    num_steps = len(new_vertices_visited)

                    # If already taken more steps than best route found for this pair of vertices, then give up.
                    if (origin, dest) in self.shortest_leg:
                        (_, best_num_steps) = self.shortest_leg[(origin, dest)]
                        if best_num_steps < num_steps:
                            return

                    # We found the destination!
                    if new_vertex == dest:
                        if (origin, dest) not in self.shortest_leg:     # First route found, so add to dictionary.
                            self.shortest_leg[(origin, dest)] = (new_keys, num_steps)
                        else:
                            # (_, best_num_steps) = self.shortest_leg[(origin, dest)]
                            if num_steps < best_num_steps:              # If better than previous best, store it.
                                self.shortest_leg[(origin, dest)] = (new_keys, num_steps)

                        # Route found, so stop searching.
                        return

                    # Recursively try route with new vertex as next waypoint on route.
                    self.find_shortest_route(origin=origin,
                                             dest=dest,
                                             waypoint=new_vertex,
                                             vertices_visited=new_vertices_visited,
                                             required_keys=new_keys)

            else:           # New vertices to try must be zero length, so stop iterating.
                iterating = False


    def print(self):
        """Send some status info to stdout."""
        print('entrance:', self.entrance,
              '   keys:', self.keys,
              '   num_keys:', self.num_keys,
              '   shortest_leg:', self.shortest_leg)

    def find_all_shortest_routes(self):
        """Find shortest routes between all pairs of places of interest on the world grid.
        Store info in shortest_leg attribute."""

        # Start by finding shortest routes from entrance to each key.
        for k_1 in self.keys:
            print('Finding shortest route from Entrance to', k_1)

            k_1_vertex = self.keys[k_1]
            self.find_shortest_route(origin=self.entrance,
                                     dest=k_1_vertex,
                                     waypoint=self.entrance,
                                     vertices_visited=[],
                                     required_keys='')

        # Now look for shortest routes between each pair of keys (in both directions).
        for k_1 in self.keys:
            for k_2 in self.keys:
                print('Finding shortest route from', k_1, 'to', k_2)

                if k_1 != k_2:                                          # No need for route from key to itself!
                    k_1_vertex = self.keys[k_1]
                    k_2_vertex = self.keys[k_2]

                    self.find_shortest_route(origin=k_1_vertex,
                                             dest=k_2_vertex,
                                             waypoint=k_1_vertex,
                                             vertices_visited=[],
                                             required_keys='')

    def collect_all_keys(self, origin: (int, int), keys_collected: str, steps_taken: int):
        """Recursive search to find shortest route that finds all of the remaining (as yet un-found) keys."""

        # Check if this is the shortest route so far from origin to last keys_collected?
        # If not, return
        if len(keys_collected) > 0:
            sorted_keys = ''.join(sorted(keys_collected))

            dest_vertex = self.keys[keys_collected[-1:]]
            if (origin, dest_vertex, sorted_keys) in self.shortest:
                shorty = self.shortest[(origin, dest_vertex, sorted_keys)]
                if steps_taken < shorty:                    # New winner!
                    self.shortest[(origin, dest_vertex, sorted_keys)] = steps_taken
                else:                                       # If not shorter than previously found, give up.
                    return
            else:
                self.shortest[(origin, dest_vertex, sorted_keys)] = steps_taken

        if self.shortest_route_steps != 0 and steps_taken >= self.shortest_route_steps:
            return

        # Work out keys that are still needed.
        keys_needed = ''
        for this_key in self.keys:
            if this_key not in keys_collected:
                keys_needed = keys_needed + this_key

        if len(keys_needed) == 0:                   # No more keys needed; all keys found.
            if self.shortest_route_steps == 0:      # No previous shortest route found. so this one must be best so far!
                self.shortest_route_steps = steps_taken
                print('Shortest route:', steps_taken)
            elif steps_taken < self.shortest_route_steps:   # New winner found.
                self.shortest_route_steps = steps_taken
                print('Shortest route:', steps_taken)
            return                                          # No more keys to find, so end the search.

        # Recursively look for routes from where we are, to each of the keys that we don't yet have.
        for this_key in keys_needed:
            key_vertex = self.keys[this_key]    # Vertex that this key is located at.
            (route_keys, route_steps) = self.shortest_leg[(origin, key_vertex)]

            # If we don't have the keys for it then, can't go there.
            have_all_keys = True
            for rk in route_keys:
                if rk not in keys_collected:
                    have_all_keys = False

            keys_collected + this_key
            if have_all_keys:
                self.collect_all_keys(origin=key_vertex,
                                      keys_collected=keys_collected + this_key,
                                      steps_taken=steps_taken + route_steps)
