# Part of solution to day 13 of AOC 2019, "Care Package".
# https://adventofcode.com/2019/day/13


class Screen:

    def __init__(self):

        self.grid = {}          # Key = (x, y), value = tile number.
        self.min_x = None
        self.min_y = None
        self.width = None
        self.height = None

    @staticmethod
    def tile_code_to_char(code: int) -> str:
        """For parm tile code, return a single char that the code can be rendered into when printing the grid.
        0 is an empty tile. No game object appears in this tile.
        1 is a wall tile. Walls are indestructible barriers.
        2 is a block tile. Blocks can be broken by the ball.
        3 is a horizontal paddle tile. The paddle is indestructible.
        4 is a ball tile. The ball moves diagonally and bounces off objects."""
        conversion_map = {0: ' ', 1: '#', 2: '%', 3: '-', 4: 'O'}
        return conversion_map[code]

    def grid_to_char(self, vertex: (int, int)) -> str:
        """For parm vertex coordinates, return char that should be rendered at that vertex."""
        return self.tile_code_to_char(self.grid.get(vertex, 0))       # Default to 0, as dict is sparse.

    def render(self, score: int):
        """Render the contents of the grid dictionary to screen. Print current game score at bottom of screen."""
        # TODO Rewrite to use Pygame to do proper graphical rendering of the game screen.
        for y in range(self.min_y, self.height + 1):
            for x in range(self.min_x, self.width + 1):
                print(self.grid_to_char(vertex=(x, y)), end='')
            print()
        print('Score:', score)                                                     # Start a new line.
