

from random import random
from SVG.scatter_plot import ScatterPlot

DOT_COUNT = 1000


def generate_scatter_plot():
    x_max = 10
    y_max = 10
    x_min = 0
    y_min = 0

    data_x = [random() * x_max for _ in range(DOT_COUNT)]
    data_y = [random() * y_max for _ in range(DOT_COUNT)]

    scatter = ScatterPlot(x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                          width=600, height=600, debug=False, title="Your Scatter Plot",
                          y_label="y axis", x_label="x axis")
    scatter.add_and_zip_data(data_x, data_y)
    scatter.build()

    scatter.save(filename="../svg_examples/scatter_plot.svg")


if __name__ == '__main__':
    generate_scatter_plot()
