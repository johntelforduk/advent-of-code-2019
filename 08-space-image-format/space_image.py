# Solution to day 8 of AOC 2019, "Space Image Format".
# https://adventofcode.com/2019/day/8

f = open('input.txt')
whole_text = (f.read())

# "The image you received is 25 pixels wide and 6 pixels tall."
width, height = 25, 6
layer_size = width * height

i = 0                                               # Position in image file.
layer, prev_layer = 0, 0                            # Layer numbers.
layer_0s, layer_1s, layer_2s = 0, 0, 0              # Layer counts.
win_0s, win_1s, win_2s = 999, 0, 0                  # Best figures found for a layer so far.

image = {}

while i < len(whole_text):
    position = i % layer_size

    pixel = whole_text[i]

    # If the pixel is opaque, and there isn't a pixel already in the image at this position.
    if pixel in {'0', '1'} and position not in image:
        image[position] = pixel

    if pixel == '0':
        layer_0s += 1

    if pixel == '1':
        layer_1s += 1

    if pixel == '2':
        layer_2s += 1

    i += 1
    layer = i // layer_size                         # // is DIV.

    if layer != prev_layer:                         # Start of a new layer.
        if layer_0s < win_0s:                       # We have a new best.
            win_0s = layer_0s
            win_1s = layer_1s
            win_2s = layer_2s
        layer_0s, layer_1s, layer_2s = 0, 0, 0      # Reset layer counts.
        prev_layer = layer

print('Part 1:', win_1s * win_2s)

# Render the image.
for i in range(layer_size):
    if image[i] == '1':
        print('#', end='')
    else:
        print(' ', end='')
    if ((i + 1) % width) == 0:
        print()
