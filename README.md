# Advent of Code 2019
Solutions to the Advent of Code 2019 puzzles.

https://adventofcode.com/2019

#### Notes

##### Day 17 "Set and Forget"
For part 2, I wrote the program *analyse.py* to find the path across the scaffolding. I then copy-and-pasted that into _check.txt_. Then I used a text editor to manually find repeating patterns in the path (it only took a few minutes to spot them). This was then used to figure out the input sent to the Intcode computer in _part_2.py_.

##### Day 19 "Tractor Beam"
I found the solution by running _part_2.py_ repeatedly, adjusting _ship_x_ and _ship_y_ by trial-and-error until the square fitted inside the beam.
