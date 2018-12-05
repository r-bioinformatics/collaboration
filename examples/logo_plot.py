import argparse
from SVG.logo_plot import Logo



def parse_arguments(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("--diversity_file", help="name of the file to process", required=True)
    parser.add_argument("--svg_file", help="name of the svg file to wtite", required=True)
    args = parser.parse_args()
    return args


Example_set = [
    {'P': 439, 'L': 63, 'S': 18, 'T': 12, 'F': 9, 'A': 12, 'Y': 5, 'V': 8, 'M': 4, 'N': 1, 'H': 5, 'K': 3, 'R': 10,
     'Q': 6, 'G': 8, 'C': 3, 'E': 3, 'W': 4, 'I': 1},
    {'L': 317, 'S': 83, 'A': 37, 'F': 4, 'R': 10, 'P': 4, 'D': 3, 'H': 6, 'G': 64, 'I': 4, 'W': 4, 'M': 22, 'K': 1,
     'T': 2, 'Q': 4, 'C': 2, 'V': 46, 'E': 1},
    {'T': 137, 'A': 136, 'M': 7, 'G': 6, 'R': 55, 'L': 28, 'Q': 5, 'F': 2, 'E': 4, 'K': 29, 'S': 62, 'P': 5, 'N': 37,
     'I': 55, 'D': 2, 'Y': 2, 'C': 1, 'V': 39, 'H': 1, 'W': 1},
    {'N': 530, 'D': 14, 'G': 8, 'I': 5, 'V': 6, 'S': 31, 'T': 7, 'R': 1, 'A': 3, 'H': 4, 'L': 2, 'K': 1, 'E': 1,
     'M': 1},
    {'T': 140, 'A': 7, 'M': 4, 'I': 4, 'L': 207, 'S': 68, 'N': 3, 'V': 91, 'G': 27, 'F': 4, 'Q': 3, 'K': 4, 'P': 4,
     'E': 1, 'W': 1, 'H': 28, 'R': 17, 'C': 1},
    {'V': 308, 'A': 43, 'S': 8, 'Y': 3, 'H': 4, 'P': 3, 'L': 5, 'F': 3, 'Q': 3, 'R': 5, 'M': 6, 'T': 161, 'G': 4,
     'K': 2, 'I': 49, 'D': 4, 'N': 2, 'W': 1},
    {'K': 491, 'G': 10, 'S': 25, 'I': 9, 'R': 15, 'E': 11, 'A': 14, 'T': 5, 'Q': 5, 'D': 1, 'P': 3, 'Y': 3, 'N': 7,
     'L': 5, 'V': 6, 'C': 1, 'W': 2, 'H': 1}]

HYDROPHOBICITY = {'L': 97,
                  'I': 99,
                  'F': 100,
                  'W': 97,
                  'V': 76,
                  'M': 75,
                  'C': 49,
                  'Y': 63,
                  'A': 41,
                  'T': 13,
                  'E': -31,
                  'G': 0,
                  'S': -5,
                  'Q': -10,
                  'D': -55,
                  'R': -14,
                  'K': -23,
                  'N': -28,
                  'H': 8,
                  'P': -46}



class LogoGraph:

    def __init__(self, data):
        self.data = data
        self.viz = Logo(units_per_bin=630, sequence_dict=Example_set)

    def run(self):
        self.viz.build()
        self.viz.save(filename="/tmp/logo_test.svg")


def main():
    # args = parse_arguments()
    #
    # # open file
    # file_handler = smart_open(args.diversity_file)

    # create analysis object
    default_class = LogoGraph(Example_set)
    default_class.run()

    # default_class.viz.save(filename=args.svg_file)


if __name__ == "__main__":
    main()
