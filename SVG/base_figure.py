
from svgwrite.shapes import Line, Rect
from svgwrite.text import Text
from svgwrite.drawing import Drawing
from svgwrite.container import Group

# pylint: disable=R0902,R0914


class Figure(object):

    def __init__(self, width=600, height=400, margin_top=20, margin_bottom=40, margin_left=40, margin_right=20,
                 x_min=0, y_min=0, x_max=1, y_max=1, debug=False, graph_colour="midnightblue", background=None,
                 x_label=None, y_label=None, y_label_max_min=True, title=None):

        self.width = width
        self.height = height
        self.debug = debug
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.x_max = x_max
        self.y_max = y_max
        self.x_min = x_min
        self.y_min = y_min
        self.graph_colour = graph_colour
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.font_size = 15

        self.plottable_x = self.width - (self.margin_left + self.margin_right)
        self.plottable_y = self.height - (self.margin_top + self.margin_bottom)

        # start drawing object
        self.plot = Drawing(debug=self.debug,
                            size=(self.width, self.height),
                            # viewBox = ("0 0 " + str(float(length) + 10) + " " + str(float(width) + 10)),
                            preserveAspectRatio="xMinYMin meet")  # , size=('200mm', '150mm'), viewBox=('0 0 200 150'))

        if background:
            self.plot.add(Rect(insert=(0, 0), size=(self.width, self.height), fill=background))

        if x_label:
            self.plottable_y -= self.font_size
            self.add_x_label()

        if y_label:
            self.plottable_x -= self.font_size
            self.margin_left += self.font_size
            self.add_y_label()

        if title:
            self.plottable_y -= self.font_size + 5
            self.margin_top += self.font_size + 5
            self.add_title()

        self.plot.add(Line(start=(self.margin_left - 4, self.margin_top),
                           end=(self.margin_left - 4, self.margin_top + self.plottable_y),
                           stroke_width=1, stroke=self.graph_colour))
        self.plot.add(Line(start=(self.margin_left, self.margin_top + self.plottable_y + 4),
                           end=(self.margin_left + self.plottable_x, self.margin_top + self.plottable_y + 4),
                           stroke_width=1, stroke=self.graph_colour))

        if y_label_max_min:
            self.add_y_max_min(self.y_max, self.y_min)

    def save(self, reset=True, filename=None):
        if filename:
            self.plot.filename = filename
        elif not self.plot.filename:
            raise Exception("No Filename set to save SVG image.")

        self.plot.save()
        print(f"wrote to {self.plot.filename}")

        if reset:
            self.plot = None

    def add_y_label(self):
        y_coord = self.margin_top + (self.plottable_y/2)
        text_group = Group(transform=f"rotate(270, {self.font_size}, {y_coord})")

        text_group.add(Text(self.y_label, insert=(0, y_coord), fill=self.graph_colour, font_size="15", stroke_width=0))
        self.plot.add(text_group)

    def add_x_label(self):
        self.plot.add(Text(self.x_label,
                           insert=(self.plottable_x / 2,
                                   self.plottable_y + self.margin_top + (self.margin_bottom / 2) + 15),
                           fill=self.graph_colour,
                           font_size=self.font_size))

    def add_title(self):
        self.plot.add(Text(self.title,
                           insert=(self.plottable_x / 2, self.font_size + 5),
                           fill=self.graph_colour,
                           font_size=self.font_size))

    def add_y_max_min(self, max_value, min_value):
        self.plot.add(Text(str(round(max_value, 2)),
                           insert=(15, self.margin_top + 15), text_anchor="end",
                           fill=self.graph_colour, font_size=self.font_size))
        self.plot.add(Text(str(min_value),
                           insert=(15, self.margin_top + self.plottable_y),
                           fill=self.graph_colour, font_size=self.font_size))

    def add_x_column_labels(self, column_positions, column_labels, rotate=None):
        for gene in column_labels:
            text_group = Group(transform=f"rotate({rotate if rotate else 0},{column_positions[gene]},"
                                         f"{self.margin_top + self.plottable_y + 17})")

            text_group.add(Text(gene, insert=(column_positions[gene], self.margin_top + self.plottable_y + 17),
                                fill=self.graph_colour, font_size=self.font_size, stroke_width=0))
            self.plot.add(text_group)

    def to_string(self, reset=True):
        string_value = self.plot.tostring()
        if reset:
            self.plot = None
        return string_value

    def add_max_min_text(self):
        self.plot.add(
            Text(str(self.x_max), insert=(self.plottable_x, self.margin_top + self.plottable_y + 20.0),
                 fill=self.graph_colour, font_size=self.font_size))
        self.plot.add(
            Text(str(self.x_min), insert=(self.margin_left, self.margin_top + self.plottable_y + 20.0),
                 fill=self.graph_colour, font_size=self.font_size))

        self.plot.add(
            Text(str(self.y_max), insert=(3, self.margin_top + 10),
                 fill=self.graph_colour, font_size=self.font_size))
        self.plot.add(
            Text(str(self.y_min), insert=(3, self.margin_top + self.plottable_y),
                 fill=self.graph_colour, font_size=self.font_size))
