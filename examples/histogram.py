""" This file generates a histogram SVG in the svg examples directory"""

from random import randrange
from SVG.histogram import Histogram


def generate_Histogram():

    hist = Histogram(units_per_bin=1, background="white")
    data = [randrange(10) for _ in range(1000)]
    hist.add_data(data)
    hist.build()
    hist.save(filename="../svg_examples/histogram.svg")


if __name__ == '__main__':
    generate_Histogram()
