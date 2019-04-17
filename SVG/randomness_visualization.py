"""
A simple plot for scattered x,y data.

"""

import math
from SVG.base_figure import Figure
from svgwrite import rgb

# pylint: disable=R0914

from svgwrite.shapes import Rect


class RandomVisualization(Figure):
    """A simple scatter diagram plot."""

    def __init__(self, x_max=100, y_max=100, width=1000, height=2000, x_min=0, y_min=0, debug=True,
                 margin_top=20, margin_bottom=30, margin_left=30, margin_right=20, background_colour="white",
                 x_label=None, y_label=None, title=None):

        Figure.__init__(self, x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                        width=width, height=height, margin_top=margin_top, margin_bottom=margin_bottom,
                        margin_left=margin_left, margin_right=margin_right, debug=debug, background=background_colour,
                        x_label=x_label, y_label=y_label, title=title)
        self.data = None

        print(f"plottable: {self.plottable_x} - {self.plottable_y}")
        self.cur_x_pos = 0
        self.cur_y_pos = 0
        self.cur_direction = True   # True = Left to Right, False = Right to Left
        self.current_map = [[0 for _y in range(self.plottable_y)] for _x in range(self.plottable_x)]
        print(f"len {len(self.current_map)} x {len(self.current_map[0])}")
        self.last_full_row = 0
        self.over_called_pixels = 0

    def put_pixels(self, colour, pixels):
        for i in range(pixels):

            if self.cur_direction:
                self.cur_x_pos += 1
            else:
                self.cur_x_pos -= 1

            if self.cur_direction and self.cur_x_pos >= self.plottable_x:
                self.cur_y_pos += 1
                self.cur_x_pos -= 1
                self.cur_direction = not self.cur_direction
            if not self.cur_direction and self.cur_x_pos < 0:
                self.cur_y_pos += 1
                self.cur_x_pos += 1
                self.cur_direction = not self.cur_direction

            self.plot.add(Rect(insert=(self.margin_left + self.cur_x_pos,
                                       (self.margin_top + self.plottable_y) - self.cur_y_pos),
                               size=(1, 1),
                               fill=rgb(colour[0], colour[1], colour[2])))

    def get_lowest_directional_pos(self, direction=True):
        for y in range(self.last_full_row, self.plottable_y):
            if direction:
                for x in range(0, self.plottable_x):
                    if self.current_map[x][y] == 0:
                        return x, y
            else:
                for x in range(self.plottable_x-1, -1, -1):
                    if self.current_map[x][y] == 0:
                        return x, y
            self.last_full_row = y
        return None, None

    def put_pixels_var1(self, colour, pixels, row_direction=True):
        hit_a_wall = False
        closest_cube = math.floor(math.sqrt(pixels))

        print(f"closest cube {closest_cube}")
        x, y = self.get_lowest_directional_pos(row_direction)
        direction = row_direction

        i = 0

        while i < pixels:

            under_pixels_used = 0
            x_other = x  # other side of the

            if direction:
                x_max = min(x + min(pixels - i, closest_cube - 1), self.plottable_x - 1)
                if row_direction and x_max == self.plottable_x - 1:
                    hit_a_wall = True
                x_min = max(0, x_max - closest_cube + 1, x - ((pixels - i) - (x_max-x)))
                inc = 1
            else:
                x_min = max(x - min(pixels - i, closest_cube - 1), 0)
                if not row_direction and x_min == 0:
                    hit_a_wall = True
                x_max = min(x_min + closest_cube - 1, x + (pixels - i) - (x-x_min))
                inc = -1

            while x_min <= x_other + inc <= x_max and self.current_map[x_other + inc][y] == 0:
                x_other += inc

            if direction:
                if x_other != x_max and x:
                    diff = x_max - x_other
                    x_min = max(x_min - diff, 0)
                    print(f"update x_min {x_min}")
            else:
                if x_other != x_min:
                    diff = x_other - x_min
                    x_max = min(diff + x_max, self.plottable_x - 1)
                    print(f"update x_max {x_max}")

            while x_min <= x - inc <= x_max and self.current_map[x - inc][y] == 0:
                x -= inc

            if y > 1:
                unused_pixel_list = []

                for pos in range(min(x, x_other), max(x, x_other)+1):
                    if self.current_map[pos][y-1] == 0:
                        under_pixels_used += 1
                        unused_pixel_list.append(pos)
                if under_pixels_used > 0:
                    for pix in unused_pixel_list:
                        self.plot.add(Rect(insert=(self.margin_left + pix,
                                                   (self.margin_top + self.plottable_y) - y + 1),
                                           size=(1, 1),
                                           fill=rgb(colour[0], colour[1], colour[2])))
                        self.current_map[pix][y-1] = 1
                    i += len(unused_pixel_list)

            print(f"writing from {min(x, x_other)} - {max(x, x_other)} in row {y} - colour {colour}")
            print(f"size ({abs(x_other-x) + 1},1)")

            for pos in range(min(x, x_other), max(x, x_other)+1):
                self.current_map[pos][y] = 1

            self.plot.add(Rect(insert=(self.margin_left + min(x, x_other),
                                       (self.margin_top + self.plottable_y) - y),
                               size=(abs(x_other-x)+1, 1),
                               fill=rgb(colour[0], colour[1], colour[2])))
            i += abs(x_other - x) + 1
            if i < 0:
                self.over_called_pixels += abs(i)

            x = max(x_other, x) if direction else min(x_other, x)
            y += 1
            direction = not direction

        return hit_a_wall
