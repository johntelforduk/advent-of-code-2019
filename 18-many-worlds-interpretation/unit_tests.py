# Part of solution to day 18 of AOC 2019, "Many-Worlds Interpretation".
# https://adventofcode.com/2019/day/18


from key_world import KeyWorld
import unittest


class TestKeyWorld(unittest.TestCase):

    def test_1(self):
        this_world = KeyWorld('test_1.txt')
        this_world.find_all_shortest_routes()
        this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
        self.assertEqual(this_world.shortest_route_steps, 8)

    def test_2(self):
        this_world = KeyWorld('test_2.txt')
        this_world.find_all_shortest_routes()
        this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
        self.assertEqual(this_world.shortest_route_steps, 86)

    def test_3(self):
        this_world = KeyWorld('test_3.txt')
        this_world.find_all_shortest_routes()
        this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
        self.assertEqual(this_world.shortest_route_steps, 132)

    def test_4(self):
        this_world = KeyWorld('test_4.txt')
        this_world.find_all_shortest_routes()
        this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
        self.assertEqual(this_world.shortest_route_steps, 136)

    def test_5(self):
        this_world = KeyWorld('test_5.txt')
        this_world.find_all_shortest_routes()
        this_world.collect_all_keys(origin=this_world.entrance, keys_collected='', steps_taken=0)
        self.assertEqual(this_world.shortest_route_steps, 81)


if __name__ == '__main__':
    unittest.main()
