
import unittest
from random import randrange
from SVG.histogram import Histogram


class TestHistogram(unittest.TestCase):

    def test_Histogram(self):

        hist = Histogram(units_per_bin=1)
        data = [randrange(10) for x in range(1000)]
        # for d in data:
        #     print(d)
        hist.add_data(data)
        hist.bin_data()
        hist.build()
        string_hist = hist.to_string()
        print(string_hist)


    def test_Histogram_2(self):

        hist = Histogram(units_per_bin=2)
        data = [randrange(10) for x in range(1000)]
        # for d in data:
        #     print(d)
        hist.add_data(data)
        hist.bin_data()
        hist.build()
        string_hist = hist.to_string()
        print(string_hist)
