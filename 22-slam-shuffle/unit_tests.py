# Part of solution to day 22 of AOC 2019, "Slam Shuffle".
# https://adventofcode.com/2019/day/22


from space_cards import SpaceCards
import unittest


class TestSpaceCards(unittest.TestCase):

    def test_new_pack(self):
        test_pack = SpaceCards(deck_size=10)
        self.assertEqual(test_pack.deck_size, 10)                           # Should be 10 cards in the pack.
        self.assertEqual(test_pack.pack, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_deal_into_new_stack(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.deal_into_new_stack()
        self.assertEqual(test_pack.pack, [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

    def test_cut_n_cards(self):
        test_pack_1 = SpaceCards(deck_size=10)
        test_pack_1.cut_n_cards(n=3)
        self.assertEqual(test_pack_1.pack, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

        test_pack_2 = SpaceCards(deck_size=10)
        test_pack_2.cut_n_cards(n=-4)
        self.assertEqual(test_pack_2.pack, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

    def test_deal_with_increment_n(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.deal_with_increment_n(n=3)
        self.assertEqual(test_pack.pack, [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

    # These tests use the example sequences of shuffles.

    def test_1(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.shuffle(filename='test_1.txt')
        self.assertEqual(test_pack.pack, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

    def test_2(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.shuffle(filename='test_2.txt')
        self.assertEqual(test_pack.pack, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])

    def test_3(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.shuffle(filename='test_3.txt')
        self.assertEqual(test_pack.pack, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])

    def test_4(self):
        test_pack = SpaceCards(deck_size=10)
        test_pack.shuffle(filename='test_4.txt')
        self.assertEqual(test_pack.pack, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])


if __name__ == '__main__':
    unittest.main()
