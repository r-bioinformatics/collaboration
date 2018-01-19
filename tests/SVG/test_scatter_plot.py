
import unittest
from random import random
from SVG.scatter_plot import ScatterPlot


DOT_COUNT = 10000


class TestScatterPlot(unittest.TestCase):

    def test_scatter_plot(self):
        x_max = 10
        y_max = 10
        x_min = 0
        y_min = 0

        data_x = [random() * x_max for _ in range(DOT_COUNT)]
        data_y = [random() * y_max for _ in range(DOT_COUNT)]

        scatter = ScatterPlot(x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                              width=600, height=400, debug=False)
        # for d in data:
        #     print(d)
        scatter.add_and_zip_data(data_x, data_y)
        scatter.build()

        # string_hist = scatter.to_string(reset=False)
        # print(string_hist)

        scatter.set_filename("/Users/anthony/temp/scatter.svg")
        scatter.save()

    def test_scatter_plot2(self):
        x_max = 10
        y_max = 10
        x_min = 5
        y_min = 5

        data_x = [random() * x_max for _ in range(DOT_COUNT)]
        data_y = [random() * y_max for _ in range(DOT_COUNT)]

        scatter = ScatterPlot(x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                              width=600, height=400, debug=False)
        # for d in data:
        #     print(d)
        scatter.add_and_zip_data(data_x, data_y)
        scatter.build()

        # string_hist = scatter.to_string(reset=False)
        # print(string_hist)

        scatter.set_filename("/Users/anthony/temp/scatter2.svg")
        scatter.save()
