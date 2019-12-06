# Solution to day 6 of AOC 2019, "Universal Orbit Map"
# https://adventofcode.com/2019/day/6


class Orbiter:

    def __init__(self, name: str, num_ancestors: int):
        """Create a new space object with parm name."""
        self.name = name
        self.my_direct_orbiters = []            # List of orbiters.
        self.num_ancestors = num_ancestors

    def add_direct_orbiter(self, name: str):
        """Add a new space object with parm name as a direct orbiter of this space object."""
        new_orbiter = Orbiter(name, num_ancestors=self.num_ancestors + 1)
        self.my_direct_orbiters.append(new_orbiter)
        return new_orbiter.num_ancestors

    def add_arbitrary_orbiter(self, parent: str, name: str):
        """Add a new space object with parm name to solar system of parm parent.
        This parent is not necessarily the current space object; nor one of its direct orbiters. It may be an
        indirect orbiter of the current space object."""
        if parent == self.name:                 # New space object has found its parent, so add it as direct orbiter.
            x = self.add_direct_orbiter(name)
        else:                                   # New space object is an indirect orbiter of this object.
            x = 0
            for satellite in self.my_direct_orbiters:
                x += satellite.add_arbitrary_orbiter(parent, name)
        return x


def is_in_system(system: Orbiter, target_name: str) -> bool:
    """Return true if there is a space object with the target name anywhere in the parm system."""

    # We found the target name in the system!
    if system.name == target_name:
        return True

    # If the names don't match, and no orbiters, then the target is not in the system.
    if system.name != target_name and len(system.my_direct_orbiters) == 0:
        return False

    # Check all of the orbiters.
    for this_satellite in system.my_direct_orbiters:
        if is_in_system(this_satellite, target_name):
            return True

    return False


def route_to_target(system: Orbiter, target_name: str, route_so_far: []) -> (bool, []):
    """Return a tuple. First element is bool which indicates if there is a route from where we are now, to the target
    space object. Second element is a list of tuples. Each of these tuples is name of object on the route, followed by
    number of ancestors that object has."""
    if system.name == target_name:
        return True, route_so_far

    for this_satellite in system.my_direct_orbiters:
        (target_found, sub_route) = route_to_target(system=this_satellite, target_name=target_name,
                                                    route_so_far=route_so_far +
                                                                 [(this_satellite.name, this_satellite.num_ancestors)])
        if target_found:
            return True, sub_route
    return False, []


f = open('input.txt')
whole_text = (f.read())
pairs = whole_text.split()                      # Split string by commas. Like ['COM)B', 'B)C'].

orbit_map = []

for each_orbit in pairs:
    split_pair = each_orbit.split(')')          # Like ['COM', 'B'].
    orbit_map.append(split_pair)

total_orbits = 0

com = Orbiter('COM', num_ancestors=0)           # First object in space has no ancestors.

# Keep trying until all space objects named in map have been added to the system.
while len(orbit_map) > 0:
    for [this_parent, this_child] in orbit_map:

        # Only attempt to add a space object to the system if it's parent is already in the system.
        if is_in_system(system=com, target_name=this_parent):
            total_orbits += com.add_arbitrary_orbiter(parent=this_parent, name=this_child)
            orbit_map.remove([this_parent, this_child])

print('Part 1:', total_orbits)

# Discard the bool that is 1st element in each tuple. Just the route lists that we need.
(_, you_route) = route_to_target(system=com, target_name='YOU', route_so_far=[])
(_, santa_route) = route_to_target(system=com, target_name='SAN', route_so_far=[])

# Find the lowest common space object in the two routes.
pos = 0
while you_route[pos] == santa_route[pos]:
    pos += 1

# Discard name of space object. Just the number of anceestors that we need.
(_, you_ancestors) = you_route[len(you_route) - 1]
(_, santa_ancestors) = santa_route[len(santa_route) - 1]

# -2 is a double gatepost adjustment, due to not needing to count position of You and Santa themselves.
min_orbital_transfers = you_ancestors + santa_ancestors - 2 * pos - 2
print('Part 2:', min_orbital_transfers)
