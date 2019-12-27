# Part of solution to day 17 of AOC 2019, "Set and Forget".
# https://adventofcode.com/2019/day/17


from ascii import Ascii

analyser = Ascii()

# analyser.load_test_screen('test_screen_1.txt')
analyser.refresh_screen()

analyser.render_screen()

analyser.turn_right()

# Find robot's path to end of scaffolding.
path_ahead = True
while path_ahead:
    analyser.forward()
    path_ahead = analyser.seek()

# Send path the robot followed to stdout.
for step in analyser.robot_trail:
    print(step, end='')
    if step not in {'R', 'L'}:
        print(' ', end='')
