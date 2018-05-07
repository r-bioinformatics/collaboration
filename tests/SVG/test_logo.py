
import unittest
from SVG.logo_plot import Logo


DOT_COUNT = 10000


class TestLogo(unittest.TestCase):

    def get_data(self, filename):
        first = True
        data = []
        headers = None
        with open(filename, "r") as test_file:
            for raw_line in test_file:
                line = raw_line.split("\t")
                print("\t".join(line))
                if first:
                    headers = line
                    first = False
                else:
                    data.append(line)

        return headers, data

    def test_scatter_plot(self):
        x_max = 10
        y_max = 10
        x_min = 0
        y_min = 0

        filename = "tests/SVG/data/pwwm1.txt"
        headers, data = self.get_data(filename)

        logo = Logo(x_max=x_max, y_max=y_max, x_min=x_min, y_min=y_min,
                    width=600, height=400, debug=False)
        # for d in data:
        #     print(d)
        logo.data_as_lists(headers[1:], data)
        logo.build()

        # string_hist = scatter.to_string(reset=False)
        # print(string_hist)

        logo.save(filename="/tmp/scatter.svg")
