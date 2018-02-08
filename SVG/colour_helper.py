"""a simple library for assigning colours."""

import random

COLOURS = {'red': ['#a30000', '#730000', '#b80000', '#660000', '#cc0000', '#520000', '#e00000', '#3d0000',
                   '#ff0a0a', '#290000', '#ff3333'],
           'blue': ['#0000a3', '#0000b8', '#00008f', '#0000cc', '#00007a', '#0000e0', '#0000f5', '#0000ff',
                    '#1f1fff', '#3333ff', '#4747ff'],
           'green': ['#00a300', '#008f00', '#002900', '#006600', '#008000', '#005200', '#00b800', '#003d00',
                     '#00cc00', '#00e000', '#33ff33'],
           'purple': ['#8f008f', '#a300a3', '#800080', '#b800b8', '#660066', '#cc00cc', '#520052', '#e000e0',
                      '#3d003d', '#290029', '#ff0aff'],
           'yellow': ['#666600', '#7a7a00', '#525200', '#8f8f00', '#3d3d00', '#cccc00'],
           'grey': ['#5c5c5c', '#525252', '#666666', '#474747', '#707070', '#3d3d3d', '#7a7a7a', '#333333',
                    '#808080', '#292929', '#8f8f8f'],
           'cyan': ['#00a3a3', '#00b8b8', '#00cccc', '#008f8f', '#00e0e0', '#007a7a', '#00f5f5', '#006666',
                    '#70ffff', '#005252', '#40bfbf'],
           'orange': ['#8f5d00', '#a36a00', '#b87700', '#7a5000', '#cc8500', '#664200', '#e09200', '#523500',
                      '#f59f00', '#3d2800', '#ffa500']}

COLOUR_INDEX = [colour for colour in COLOURS.keys()]


class ColourHelper(object):

    def __init__(self):
        self.sample_index = {}

    def add_sample_random(self, category, sample_name):
        colour = '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if category not in self.sample_index:
            self.sample_index[category] = {}
        self.sample_index[category][sample_name] = colour

    def add_sample(self, category, sample_name, category_group=False):

        if category not in self.sample_index:
            category_colour = COLOUR_INDEX[len(self.sample_index) % len(COLOUR_INDEX)]
            self.sample_index[category] = {'colour': category_colour}
        else:
            category_colour = self.sample_index[category]['colour']

        if category_group:
            self.sample_index[category][sample_name] = category_colour
        else:
            select_colour = (len(self.sample_index[category])-1) % len(COLOURS[category_colour])
            self.sample_index[category][sample_name] = COLOURS[category_colour][select_colour]

    def get_colour(self, category, sample_name):
        return self.sample_index[category][sample_name]

    def get_category_colour(self, category):
        return self.sample_index[category]['colour']
