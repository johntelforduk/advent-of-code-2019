# Part of solution to day 22 of AOC 2019, "Slam Shuffle".
# https://adventofcode.com/2019/day/22


class SpaceCards:

    def __init__(self, deck_size: int):

        self.deck_size = deck_size

        # "Just like any deck of space cards, there are 10007 cards in the deck numbered 0 through 10006. The deck must
        # be new - they're still in factory order, with 0 on the top, then 1, then 2, and so on, all the way through to
        # 10006 on the bottom."

        self.pack = []
        for i in range(deck_size):
            self.pack.append(i)

    def deal_into_new_stack(self):
        # "... create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly
        # until you run out of cards".
        self.pack.reverse()

    def cut_n_cards(self, n: int):
        # "... take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck,
        # retaining their order."

        # "You've also been getting pretty good at a version of this technique where N is negative! In that case, cut
        # (the absolute value of) N cards from the bottom of the deck onto the top."
        if n >= 0:
            cut_point = n
        else:
            cut_point = self.deck_size + n

        new_pack = []
        for i in range(cut_point, self.deck_size):      # Cards below cut.
            new_pack.append(self.pack[i])
        for i in range(cut_point):
            new_pack.append(self.pack[i])                          # Cards above cut.

        self.pack = new_pack

    def deal_with_increment_n(self, n: int):
        # "... start by clearing enough space on your table to lay out all of the cards individually in a long line.
        # Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card
        # there. If you would move into a position past the end of the space on your table, wrap around and keep
        # counting from the leftmost card again. Continue this process until you run out of cards."

        # Start by making space for new pack.
        new_pack = []
        for i in range(self.deck_size):
            new_pack.append(-1)                 # Doesn't matter what each element is initialised to.

        curr_pos = 0
        for i in self.pack:
            assert new_pack[curr_pos] == -1            # Should not be a card in this position aleady.
            new_pack[curr_pos] = i

            curr_pos = (curr_pos + n) % self.deck_size        # Move to next position.

        self.pack = new_pack.copy()

    def shuffle(self, filename: str):
        f = open(filename)
        whole_text = f.read()
        f.close()

        for each_line in whole_text.split('\n'):

            word_list = list(each_line.split(' '))

#            print(each_line, word_list)

            if word_list[0] == 'cut':
                self.cut_n_cards(n=int(word_list[1]))
            elif word_list[1] == 'into':
                self.deal_into_new_stack()
            else:
                self.deal_with_increment_n(n=int(word_list[3]))
