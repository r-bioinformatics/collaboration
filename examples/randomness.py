import argparse
import math
from smart_open import smart_open
from SVG.randomness_visualization import RandomVisualization


def parse_arguments(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("--diversity_file", help="name of the file to process", required=True)
    parser.add_argument("--svg_file", help="name of the svg file to wtite", required=True)
    args = parser.parse_args()
    return args


aa_to_int = {
    'L': 0,
    'I': 1,
    'F': 2,
    'W': 3,
    'V': 4,
    'M': 5,
    'C': 6,
    'Y': 7,
    'A': 8,
    'T': 9,
    'E': 10,
    'G': 11,
    'S': 12,
    'Q': 13,
    'D': 14,
    'R': 15,
    'K': 16,
    'N': 17,
    'H': 18,
    'P': 19}


ITEMS_TO_DISPLAY = 100


class RandomnessGenerator:

    def __init__(self, file):
        self.viz = RandomVisualization()
        self.data = None
        self.file = file
        self.read_sequences_from_file()

    def read_sequences_from_file(self):
        diversity_yet = False
        sequences = []
        for line in self.file:
            line = line.decode("utf-8").strip()
            if not diversity_yet:
                if line.find("-------------") >= 0:
                    diversity_yet = True
                continue
            pieces = line.split(" ")
            if len(pieces) < 2:
                continue
            if pieces[1] == "Discarded":
                continue
            sequences.append({'len': int(pieces[0]),
                              'seq': pieces[1]})
        self.data = sequences

    @staticmethod
    def seq_to_colour(seq):
        if len(seq) != 7:
            return None

        r = math.floor((aa_to_int[seq[0]] + aa_to_int[seq[1]]) * 6.35)
        g = math.floor((aa_to_int[seq[2]] + aa_to_int[seq[3]]) * 6.35)
        b = math.floor((aa_to_int[seq[4]] + aa_to_int[seq[5]] + aa_to_int[seq[6]]) * 4.25)

        colour = (r, g, b)
        return colour

    def run(self):
        row_direction = True
        for item in self.data:
            hit_a_wall = False
            pixels = item['len']
            seq = item['seq']
            colour = self.seq_to_colour(seq)
            if colour:
                hit_a_wall = self.viz.put_pixels_var1(colour, pixels, row_direction)
            if hit_a_wall:
                row_direction = not row_direction


def main():
    args = parse_arguments()

    # open file
    file_handler = smart_open(args.diversity_file)

    # create analysis object
    default_class = RandomnessGenerator(file_handler)
    default_class.run()

    default_class.viz.save(filename=args.svg_file)

    print(f"{default_class.viz.over_called_pixels} pixels overrepresented.")


if __name__ == "__main__":
    main()
