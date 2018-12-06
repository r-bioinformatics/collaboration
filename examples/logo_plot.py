import argparse
from SVG.logo_plot import Logo


def parse_arguments(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("--diversity_file", help="name of the file to process", required=True)
    parser.add_argument("--svg_file", help="name of the svg file to wtite", required=True)
    args = parser.parse_args()
    return args


weighted_cluster_set = [
    {'R': 45725, 'P': 39029, 'G': 15304, 'L': 15028, 'V': 4125, 'K': 3817, 'S': 3603, 'E': 2903, 'A': 2454, 'Y': 1594,
     'F': 1506, 'W': 1275, 'Q': 1157, 'T': 1122, 'C': 944, 'I': 852, 'M': 718, 'H': 412, 'N': 169, 'D': 122},
    {'K': 40690, 'L': 21578, 'R': 21118, 'S': 9983, 'V': 9220, 'G': 8625, 'I': 4017, 'Y': 3933, 'A': 3806, 'F': 3350,
     'T': 3106, 'M': 2334, 'H': 2010, 'W': 1596, 'E': 1438, 'C': 1265, 'P': 1255, 'Q': 1175, 'N': 788, 'D': 572},
    {'V': 22978, 'G': 12610, 'Y': 12145, 'T': 11702, 'S': 10706, 'I': 8340, 'R': 8272, 'A': 8168, 'H': 7934, 'K': 6914,
     'L': 6441, 'F': 5322, 'C': 4104, 'W': 3216, 'N': 3191, 'M': 2875, 'E': 2223, 'Q': 2054, 'P': 1608, 'D': 1056},
    {'N': 40543, 'H': 32532, 'Q': 10737, 'I': 9220, 'S': 7655, 'K': 6554, 'R': 5320, 'G': 4530, 'A': 4021, 'P': 3434,
     'V': 3271, 'T': 2969, 'M': 2964, 'D': 2049, 'Y': 1924, 'L': 1833, 'C': 884, 'E': 807, 'W': 309, 'F': 303},
    {'S': 21764, 'I': 19406, 'G': 18420, 'L': 13976, 'T': 10321, 'K': 10284, 'A': 10257, 'V': 10002, 'N': 7452,
     'R': 5092, 'M': 2825, 'Q': 2222, 'D': 2117, 'P': 1947, 'F': 1298, 'E': 1276, 'H': 1189, 'W': 756, 'Y': 674,
     'C': 581},
    {'V': 29464, 'T': 23219, 'E': 17360, 'D': 13047, 'A': 11431, 'S': 9354, 'L': 7002, 'P': 6278, 'G': 6132, 'I': 4629,
     'R': 4224, 'K': 2691, 'N': 2073, 'H': 1422, 'F': 946, 'M': 865, 'Q': 679, 'W': 543, 'Y': 278, 'C': 222},
    {'K': 44417, 'V': 25902, 'E': 8765, 'A': 8304, 'S': 7487, 'R': 7348, 'L': 7254, 'D': 5479, 'T': 5138, 'P': 4660,
     'I': 4359, 'M': 3188, 'G': 2955, 'Q': 2481, 'N': 1284, 'W': 1092, 'C': 925, 'F': 450, 'Y': 221, 'H': 150}]

Cluster_set = [
    {'P': 6928, 'R': 6317, 'L': 4777, 'G': 3511, 'S': 1697, 'V': 1436, 'A': 1256, 'E': 1153, 'K': 1017, 'F': 719,
     'C': 505, 'T': 504, 'W': 472, 'Q': 431, 'Y': 395, 'I': 373, 'H': 256, 'M': 234, 'N': 119, 'D': 90},
    {'R': 5426, 'L': 4786, 'V': 3145, 'G': 3027, 'S': 2818, 'K': 2628, 'A': 1426, 'I': 1182, 'F': 1074, 'Y': 954,
     'T': 954, 'W': 791, 'E': 672, 'C': 667, 'P': 606, 'H': 505, 'Q': 490, 'M': 459, 'N': 294, 'D': 286},
    {'G': 4433, 'R': 3288, 'V': 3165, 'S': 3086, 'L': 2465, 'A': 2190, 'I': 1866, 'T': 1806, 'K': 1440, 'H': 1285,
     'Y': 1106, 'E': 1053, 'N': 955, 'F': 831, 'C': 781, 'Q': 644, 'P': 569, 'M': 465, 'W': 462, 'D': 300},
    {'N': 7986, 'I': 2936, 'S': 2655, 'R': 2205, 'G': 2089, 'H': 2076, 'K': 1551, 'A': 1532, 'V': 1233, 'M': 1182,
     'L': 1051, 'T': 1050, 'Q': 1032, 'P': 912, 'D': 795, 'Y': 640, 'E': 457, 'C': 453, 'W': 189, 'F': 166},
    {'S': 4294, 'G': 3757, 'L': 3233, 'K': 2838, 'A': 2782, 'V': 2678, 'T': 2227, 'R': 2180, 'N': 1790, 'I': 1570,
     'P': 848, 'M': 595, 'E': 566, 'Q': 552, 'F': 501, 'W': 423, 'D': 395, 'H': 345, 'C': 321, 'Y': 295},
    {'V': 7733, 'T': 4002, 'A': 3819, 'S': 2744, 'L': 2399, 'G': 1819, 'I': 1473, 'R': 1317, 'D': 1258, 'E': 1182,
     'P': 1010, 'K': 823, 'N': 567, 'F': 445, 'H': 386, 'M': 311, 'Q': 276, 'W': 275, 'Y': 182, 'C': 169},
    {'K': 10610, 'V': 3408, 'R': 2921, 'S': 2239, 'A': 2045, 'G': 1621, 'E': 1606, 'T': 1427, 'L': 1157, 'I': 996,
     'P': 792, 'Q': 750, 'D': 719, 'N': 394, 'M': 389, 'C': 369, 'W': 256, 'F': 221, 'Y': 149, 'H': 121}]

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
        self.viz = Logo(units_per_bin=630, sequence_dict=weighted_cluster_set)

    def run(self):
        self.viz.build()
        self.viz.save(filename="/tmp/weighted_cluster_test.svg")


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
