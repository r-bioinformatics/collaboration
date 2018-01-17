"""
A simple plot for scattered x,y data.

"""
from svgwrite.shapes import Line
from svgwrite.shapes import Circle
from svgwrite.text import Text
from SVG.base_figure import Figure


class ScatterPlot(Figure):
    """A simple scatter diagram plot."""

    def __init__(self, x_max=100, y_max=100, width=1800, height=900, x_min=0, y_min=0, debug=True,
                 margin_top=20, margin_bottom=30, margin_left=30, margin_right=20, background_colour="white",
                 autoscale=False, x_label=None, y_label=None):
        """
        Initialize this object - you need to pass it a mongo object for it to
        operate on.
        """
        Figure.__init__(self, x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                        width=width, height=height, margin_top=margin_top, margin_bottom=margin_bottom,
                        margin_left=margin_left, margin_right=margin_right, debug=debug, background=background_colour,
                        x_label=x_label, y_label=y_label)
        self.data = None
        self.autoscale = autoscale
        self.add_max_min_text()

    def add_and_zip_data(self, x, y):
        """adds the data to the scatter plot, using zip to assemble the x and y's."""
        self.data = list(zip(x, y))

    # def add_data(self, x):
    #     """adds the data to the scatter plot - no zipping applied."""
    #     self.data = x

    def add_zero_based_regression(self, slope):
        """place a regression line on the plot."""
        self.max_min()
        x = self.x_max
        y = slope * x

        if y > self.y_max:
            y = self.y_max
            x = y / slope

        self.plot.add(Line(start=(self.margin_left, self.margin_top + self.plottable_y),
                           end=(self.x_to_printx(x), self.y_to_printy(y)),
                           stroke_width=1, stroke=self.graph_colour))

        self.plot.add(
            Text("Slope = {}".format(round(slope, 4)),
                 insert=(self.plottable_x + self.margin_left - 200, self.margin_top + 15),
                 fill=self.graph_colour, font_size="15"))

    def x_to_printx(self, x):
        """transforms the x value to an x coordinate"""
        return self.margin_left + (((float(x)-self.x_min) / (self.x_max - self.x_min)) * self.plottable_x)

    def y_to_printy(self, y):
        """transforms the y value to a y coordinate"""
        return (self.margin_top + self.plottable_y) - (((float(y)-self.y_min) /
                                                        (self.y_max-self.y_min)) * self.plottable_y)

    def max_min(self):
        """Find Max values for x and y dimensions"""
        self.x_max = self.data[0][0]
        self.y_max = self.data[0][1]
        for x, y in self.data:
            if x > self.x_max:
                self.x_max = x
            if y > self.y_max:
                self.y_max = y
        # print("max x y : {} {}".format(self.x_max, self.y_max))y_max

    def build(self):
        """assembles the data in the scatterplot, adding the points as circles."""
        if self.autoscale:
            self.max_min()
        for row in self.data:
            x = row[0]
            y = row[1]

            if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:

                x_plot = self.x_to_printx(x)
                y_plot = self.y_to_printy(y)

                self.plot.add(Circle(center=(x_plot, y_plot),
                                     r=2,
                                     stroke_width=0.1,
                                     stroke_linecap='round',
                                     stroke_opacity=0.5,
                                     fill="dodgerblue",
                                     fill_opacity=0.5))

        self.data = None
