"""Class for generating in-house Histograms"""

import math
from svgwrite.shapes import Rect
from svgwrite.text import Text
from SVG.base_figure import Figure

# pylint: disable=R0902,R0914


class Histogram(Figure):

    def __init__(self, units_per_bin, width=800, height=600, debug=False, gap=5, x_min=None, x_max=None, y_min=0,
                 y_max=0, margin_top=20, margin_bottom=40, margin_left=20, margin_right=20, x_label="x_label",
                 y_label="y_label", graph_colour="midnightblue", background="white", title="Your Histogram"):
        Figure.__init__(self, width=width,
                        height=height,
                        margin_top=margin_top,
                        x_max=x_max,
                        y_max=y_max,
                        x_min=x_min,
                        y_min=y_min,
                        margin_bottom=margin_bottom,
                        margin_left=margin_left,
                        margin_right=margin_right,
                        debug=debug,
                        graph_colour=graph_colour,
                        background=background,
                        y_label=y_label,
                        x_label=x_label,
                        title=title)
        self.units_per_bin = units_per_bin
        self.data_max = 0

        self.gap = gap
        self.height = height
        self.debug = debug

        self.data = []
        self.binned_data = None

    def add_data(self, data_set):
        self.data = data_set

    def add_data_point(self, data_point):
        self.data.append(data_point)

    def build(self):
        if not self.data:
            raise Exception("No data provided for histogram.")

        if self.x_max is None:
            self.x_max = math.ceil(max(self.data))
        if self.x_min is None:
            self.x_min = math.floor(min(self.data))
        how_many_bins = int(math.ceil((float(self.x_max) - self.x_min) / self.units_per_bin))

        self.binned_data = {}
        for i in range(how_many_bins + 1):
            self.binned_data[i] = 0

        for x_value in self.data:
            if x_value > self.x_max:
                continue
            bin_num = int(math.floor((x_value - self.x_min) / self.units_per_bin))
            self.binned_data[bin_num] += 1  # floored division.
        self.data_max = max(self.binned_data.values())

        bin_count = len(self.binned_data) + 1
        bin_width = (self.plottable_x - (bin_count + 1) + self.gap) // bin_count  # floored division

        if self.y_label_max_min and not self.y_max:
            self.y_max = 0
            for count in self.binned_data.values():
                if count > self.y_max:
                    self.y_max = count
        if self.y_label_max_min and not self.y_min:
            self.y_min = 0
            for count in self.binned_data.values():
                if count < self.y_min:
                    self.y_min = count

        if self.y_label_max_min:
            self.add_y_max_min(self.y_max, self.y_min)

        if bin_width < 1:
            bin_width = 1
        for i in range(len(self.binned_data)):
            self.plot.add(Rect(insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                       (self.margin_top + self.plottable_y) - ((float(self.binned_data[i])
                                                                                / self.data_max) * self.plottable_y)),
                               size=(bin_width, ((float(self.binned_data[i]) / self.data_max) * self.plottable_y)),
                               fill="red"))
            self.plot.add(Text(str((i * self.units_per_bin) + self.x_min),
                               insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                       self.plottable_y + self.margin_top + 20),
                               fill=self.graph_colour, font_size="15"))

        self.data = None
