# Part of solution to day 13 of AOC 2019, "Care Package".
# https://adventofcode.com/2019/day/13

from intcode_computer import dict_computer as comp
import screen


class Game:

    def __init__(self, filename: str):
        self.comp = comp.Computer(output_to_screen=False)   # The game needs a computer to run game logic.
        self.comp.load_file(filename)                       # Load program from parm filename into computer memory.
        self.scr = screen.Screen()                          # The game needs a screen.
        self.ball = (0, 0)                                  # Current (x, y) position of the ball.
        self.paddle = (0, 0)                                # Current (x, y) position of the paddle.
        self.score = 0                                      # Player's score.
        self.frames = 0                                     # Number of frames so far.

    def ai_player(self):
        """An automatic player of the game."""

        # Decision making is entirely based on positions of paddle and ball in x-axis.
        (paddle_x, _) = self.paddle
        (ball_x, _) = self.ball

        if ball_x < paddle_x:
            self.comp.input = -1            # "If the joystick is tilted to the left, provide -1."
        elif ball_x > paddle_x:
            self.comp.input = 1             # "If the joystick is tilted to the right, provide 1."
        else:
            self.comp.input = 0             # "If the joystick is in the neutral position, provide 0."

    def run(self):
        waltzer = 0                         # Cycles through 0, 1, 2, 0, 1, 2, 0, ...
        triplet = []                        # List of [x, y, tile_code]. Reset to empty list whenever waltzer is reset.

        while not self.comp.halted:
            self.comp.tick()                # Make the computer execute one instruction.
            if self.comp.new_output:        # Something has changed on screen, so re-render it.

                triplet.append(self.comp.output)

                waltzer = (waltzer + 1) % 3     # Increment waltzer. Reset it to zero when it gets to 3.
                if waltzer == 0:
                    assert len(triplet) == 3
                    x = triplet[0]
                    y = triplet[1]
                    tile = triplet[2]
                    triplet = []                            # Reset the triplet list.

                    # When three output instructions specify X=-1, Y=0, the third output instruction is not a tile;
                    # the value instead specifies the new score to show in the segment display.

                    if x == -1 and y == 0:
                        self.score = tile
                    else:                                   # Normal output, which is tiles to be added to screen grid.
                        self.scr.grid[(x, y)] = tile

                        if self.scr.min_x is None or x < self.scr.min_x:
                            self.scr.min_x = x
                        if self.scr.min_y is None or y < self.scr.min_y:
                            self.scr.min_y = y
                        if self.scr.width is None or x > self.scr.width:
                            self.scr.width = x
                        if self.scr.height is None or y > self.scr.height:
                            self.scr.height = y

                        if tile == 3:                       # Tile code for paddle.
                            self.paddle = (x, y)
                        elif tile == 4:                     # Tile code for ball.
                            self.ball = (x, y)

                        # In AI mode, only render 1 in 10 frames.
                        if not self.comp.input_from_keyboard and (self.frames % 10) == 0:
                            self.scr.render(self.score)     # Screen grid has changed, so re-render the screen.
                        self.frames += 1

            if not self.comp.input_from_keyboard:           # User is not controlling the paddle...
                self.ai_player()                            # ... so get the AI to control it.

        self.scr.render(self.score)                         # Ensure the very last frame is rendered.
