"""Class for generating in-house Histograms"""

import statistics
from svgwrite.shapes import Circle, Rect
from svgwrite.text import Text
from svgwrite.path import Path
from SVG.base_figure import Figure
from SVG.colour_helper import ColourHelper


class GeneCompare(Figure):

    def __init__(self, x_categories, width=1800, height=900, debug=False, gap=5, x_min=None, x_max=None,
                 y_min=0, y_max=0, margin_top=20, margin_bottom=155, margin_left=20, margin_right=20, x_label="x_label",
                 y_label=None, graph_colour="black", background_colour="white"):
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
                        background=background_colour,
                        x_label=x_label,
                        y_label=y_label)
        self.x_categories = x_categories
        self.data_max = 0

        self.gap = gap
        self.height = height
        self.debug = debug

        self.data = []
        self.legend = {}
        self.colour_helper = ColourHelper()
        self.gene_list = []

    def add_data(self, x):
        self.data = x

    def add_legend_point(self, sample_name, category, sample_num):
        self.legend[sample_name] = {'colour': None,
                                    'category': category,
                                    'number': sample_num}

    def add_data_point(self, gene, sample_num, value):
        self.data.append((gene, sample_num, value))
        if gene not in self.gene_list:
            self.gene_list.append(gene)

    def scale_y(self, value, max_value, min_value):
        return float(self.plottable_y) * (value-min_value) / (max_value - min_value)

    def build(self, reset=True):
        self.assign_colours()

        self.plottable_x = self.plottable_x - 150

        self.add_legend()

        values = {}

        # dats points
        for item in self.data:
            gene = item[0]
            category = self.legend[item[1]]['category']
            if gene not in values:
                values[gene] = {}
            if category not in values[gene]:
                values[gene][category] = []
            values[gene][category].append(float(item[2]))

        max_value = -99999999999999
        min_value = 0
        for gene in values:
            for category in values[gene]:
                max_gene = max(values[gene][category])
                if max_gene > max_value:
                    max_value = max_gene

        self.gene_list = sorted(self.gene_list)
        num_columns = len(self.gene_list)
        column_pos = {}
        for idx, gene in enumerate(self.gene_list):
            column_pos[gene] = ((idx+1) * self.plottable_x/(num_columns + 1)) + self.margin_left

        self.plot_data(column_pos, max_value, min_value)
        self.add_x_column_labels(column_pos, self.gene_list, rotate=90)
        self.add_y_max_min(max_value, min_value)
        self.add_gausian_lines(column_pos, max_value, min_value, values)

        # self.plot.add(Text(,
        #                    insert=(self.margin_left + self.gap,
        #                            self.plottable_y + self.margin_top + 20),
        #                    fill="yellow", font_size="15"))
        if reset:
            self.data = None

    def add_gausian_lines(self, column_pos, max_value, min_value, values):
        for gene in values:
            for category in values[gene]:
                gene_values = values[gene][category]
                if len(gene_values) > 1:
                    stddev = statistics.stdev(gene_values)
                    median = statistics.median(gene_values)
                    colour = self.colour_helper.get_category_colour(category)
                    scale_x = 1
                    scale_y = float(self.plottable_y) / (max_value - min_value)
                    d = self.calculate_gausian_curve(pos=column_pos[gene],
                                                     height=30,
                                                     stddev=stddev,
                                                     scale_x=scale_x,
                                                     scale_y=scale_y,
                                                     horizontal=False,
                                                     median=median)
                    self.plot.add(Path(stroke=colour,
                                       stroke_width=2,
                                       stroke_linecap='round',
                                       stroke_opacity=0.5,
                                       fill=colour,
                                       fill_opacity=0.1,
                                       d=d))

    def plot_data(self, column_pos, max_value, min_value):
        for item in self.data:
            gene = item[0]
            sample_name = item[1]
            value = item[2]
            colour = self.legend[sample_name]['colour']
            self.plot.add(Circle(center=(column_pos[gene],
                                         self.margin_top + self.plottable_y -
                                         self.scale_y(value, max_value, min_value)),
                                 r=3,
                                 stroke_width=0.1,
                                 stroke_linecap='round',
                                 stroke_opacity=1,
                                 fill=colour,
                                 fill_opacity=0.6))  # set to 0.2 if you want to show clear.

    def assign_colours(self):
        for sample_name in self.legend:
            category = self.legend[sample_name]['category']
            self.colour_helper.add_sample(category, sample_name)
            self.legend[sample_name]['colour'] = self.colour_helper.get_colour(category, sample_name)

    def add_legend(self):
        # legend:
        for idx, sample_name in enumerate(sorted(self.legend)):
            self.plot.add(Text(sample_name + " [" + self.legend[sample_name]['category'] + "]",
                               insert=(self.margin_left + self.plottable_x + 10,
                                       self.margin_top + self.plottable_y / 10 + (idx * 15)),
                               fill=self.graph_colour,
                               font_size="15"))
            self.plot.add(Rect(insert=(self.margin_left + self.plottable_x,
                                       self.margin_top + self.plottable_y / 10 + (idx * 15) - 9),
                               size=(8, 8),
                               fill=self.legend[sample_name]['colour']))

    def calculate_gausian_curve(self, pos, height, stddev, scale_x, scale_y, horizontal=True, median=0, sigmas=3, shift=8):
        """ path points will be at (-3stddev,0), (0,height), (3stddev,0)
            Control points at (-1stddev,0), (-1stddev,height), (1stddev,height), (1stddev,0)
         """

        curve_dist = [-sigmas * stddev, -1 * stddev, -1 * stddev, 0, stddev, stddev, sigmas * stddev]
        curve_heights = [0, 0, height, height, height, 0, 0]

        if horizontal is True:
            x_axis_values = [round((x - self.margin_left + pos) * scale_x, 2) + self.margin_left for x in curve_dist]
            # Scale Y and inverse the coordinates
            y_temp = [round(y1 * scale_y, 2) for y1 in curve_heights]
            y_axis_values = [(self.plottable_y - self.margin_top - y2) for y2 in y_temp]

        else:
            x_axis_values = [round(((pos - self.margin_left) * scale_x) + y
                                   + self.margin_left + shift, 2) for y in curve_heights]
            y_temp = [(cd + median) * scale_y for cd in curve_dist]
            y_axis_values = [round((self.margin_top + self.plottable_y - y2), 2) for y2 in y_temp]

        d = "M " + str(x_axis_values[0]) + "," + str(y_axis_values[0]) + " C"  # point 1
        for i in range(1, 7):
            d += " " + str(x_axis_values[i]) + "," + str(y_axis_values[i])
        return d

    def save(self, reset=True):
        super().save(reset)

    def set_filename(self, filename):
        super().set_filename(filename)
