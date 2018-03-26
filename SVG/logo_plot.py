"""Class for generating in-house Histograms"""

from svgwrite.shapes import Rect
from svgwrite.text import Text
from SVG.base_figure import Figure


class Logo(Figure):

    def __init__(self, units_per_bin, width=800, height=600, debug=False, gap=5, x_min=None, x_max=None, y_min=0,
                 y_max=0, margin_top=20, margin_bottom=40, margin_left=20, margin_right=20, x_label=None,
                 graph_colour="midnight_blue"):
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
                        graph_colour=graph_colour)
        self.units_per_bin = units_per_bin
        self.data_max = 0

        self.gap = gap
        self.height = height
        self.debug = debug

        self.data = []
        self.binned_data = None
        self.x_label = x_label

        self.alphabet = []

    def data_as_dicts(self, alphabet, data):
        self.alphabet = alphabet  # ordered list of alphabet symbols
        self.data = data

    def data_as_lists(self, alphabet, data):
        self.alphabet = alphabet
        self.data = data

    def build(self):
        bin_count = len(self.data) + 1
        bin_width = (self.plottable_x - (bin_count + 1) + self.gap) // bin_count  # floored division
        if bin_width < 1:
            bin_width = 1
        for i in range(len(self.data)):

            for letter in self.alphabet:
                size = float(self.data[letter]) * self.plottable_y
                self.plot.add(Text(letter),
                              insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                      self.plottable_y + self.margin_top + 20),
                              fill="yellow", height=size)





            self.plot.add(Rect(insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                       (self.margin_top + self.plottable_y) - ((float(self.binned_data[i])
                                                                                / self.data_max) * self.plottable_y)),
                               size=(bin_width, ((float(self.binned_data[i]) / self.data_max) * self.plottable_y)),
                               fill="red"))
            self.plot.add(Text(str((i * self.units_per_bin) + self.x_min),
                               insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                       self.plottable_y + self.margin_top + 20),
                               fill="yellow", font_size="15"))
            self.plot.add(Text(self.x_label,
                          insert=(self.plottable_x/2,
                                  self.plottable_y + self.margin_top + (self.margin_bottom/2) + 15),
                          fill="yellow",
                          font_size="15"))
            self.plot.add(Text(str()))
        self.data = None

    def save(self, reset=True):
        super().save(reset)

    def set_filename(self, filename):
        super().set_filename(filename)
