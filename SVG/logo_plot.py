"""Class for generating in-house Histograms"""

from svgwrite.text import Text
from SVG.base_figure import Figure
from svgwrite import rgb


# pylint: disable=R0902,R0914


HYDROPHOBICITY_COLOUR = {'L': (0, 0, 255),
                         'I': (0, 0, 255),
                         'F': (0, 0, 255),
                         'W': (0, 0, 255),
                         'V': (0, 125, 255),
                         'M': (0, 255, 255),
                         'C': (0, 255, 0),
                         'Y': (0, 255, 0),
                         'A': (0, 255, 0),
                         'T': (255, 125, 0),
                         'E': (255, 0, 0),
                         'G': (0, 255, 0),
                         'S': (125, 255, 0),
                         'Q': (125, 255, 0),
                         'D': (255, 0, 0),
                         'R': (200, 200, 0),
                         'K': (200, 200, 0),
                         'N': (200, 200, 0),
                         'H': (125, 75, 0),
                         'P': (255, 0, 0)}


class Logo(Figure):

    def __init__(self, units_per_bin, sequence_dict, width=800, height=600, debug=False, gap=5, x_min=None,
                 x_max=None, y_min=0,
                 y_max=0, margin_top=20, margin_bottom=40, margin_left=20, margin_right=20, x_label=None,
                 graph_colour="black"):
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

        self.data = sequence_dict
        self.binned_data = None
        self.x_label = x_label

    def build(self):
        bin_count = len(self.data) + 1
        bin_width = (self.plottable_x - (bin_count + 1) + self.gap) // bin_count  # floored division
        if bin_width < 1:
            bin_width = 1
        for i in range(len(self.data)):
            s = sum([v for k, v in self.data[i].items()])
            bottom = self.plottable_y + self.margin_top
            for letter, value in sorted(list(self.data[i].items()), key=lambda x: -x[1]):
                size = float(self.data[i][letter]/s) * self.plottable_y
                if size < 10:
                    continue
                colour = HYDROPHOBICITY_COLOUR[letter]
                self.plot.add(Text(letter,
                                   insert=(self.margin_left + self.gap + (i * (bin_width + self.gap)),
                                           bottom),
                                   lengthAdjust="spacingAndGlyphs", textLength=80,
                                   fill=rgb(colour[0], colour[1], colour[2]), font_size=f"{size/10.75}em"))
                bottom -= size
            self.plot.add(Text(str()))
        self.data = None
