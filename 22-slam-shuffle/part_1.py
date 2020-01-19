# Part of solution to day 22 of AOC 2019, "Slam Shuffle".
# https://adventofcode.com/2019/day/22


from space_cards import SpaceCards

# "After shuffling your factory order deck of 10007 cards, what is the position of card 2019?"

this_pack = SpaceCards(deck_size=10007)
this_pack.shuffle('input.txt')

for i in range(this_pack.deck_size):
    if this_pack.pack[i] == 2019:
        print('Part 1:', i)
