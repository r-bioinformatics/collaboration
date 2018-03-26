

from svgwrite.shapes import Rect
from svgwrite.text import Text
from svgwrite.drawing import Drawing
from math import fabs

import time
from SVG.plot_utilities import add_cpg, get_axis, bigfont, medfont, smallfont, legend_color


class Plot(object):
    """
    Called byrapper object to plot methylation data.
    """

    METHYLATION_DOT_RADIUS = 2
    METHYLATION_DISTR_HT_MED = 12.0
    METHYLATION_DISTR_HT_BIG = 24.0
    DISTR_SHIFT = 0
    DISTR_STROKE = 0.75
    BOTTOM_MARGIN = 120  # 120 pixels
    RIGHT_MARGIN = 30
    MARGIN = 30
    GENE_OFFSET = 20

    def __init__(self):
        """Simple initiation of all of the self parameters... Does not do anything unexpected."""
        self.elements = []
        self.title = None
        self.sample_grouping = {}  # store sample id/sample group.
        self.gausian_colour = {}
        self.last_hash = 0
        self.start = 0
        self.end = 0
        self.width = 200  # default = 200.0

        self.height = 60  # default = 60.0
        self.message = None

        self.dimension_y = 0  # this is the size of the y field
        self.dimension_x = 0
        self.scale_x = 0
        self.y_bottom = "0"

        self.scale_y = 0
        self.maxh = 0
        self.plot = None

        self.gene_offset = self.GENE_OFFSET

    def set_properties(self, filename, title, start, end, width, height):
        """Set the properties of the canvas on which you'll want to generate your image """
        self.elements = []
        self.title = title
        self.start = start
        self.end = end
        self.width = width  # default = 200.0

        self.height = height  # default = 60.0

        self.dimension_y = self.height - self.MARGIN - self.BOTTOM_MARGIN  # this is the size of the y field
        self.dimension_x = self.width - self.MARGIN - self.RIGHT_MARGIN
        self.scale_x = float(self.dimension_x) / (self.end - self.start)  # this is a scaling variable
        self.y_bottom = str(round(self.dimension_y + self.MARGIN, 2))

        canvas_size = (str(self.width) + "px", "100%")
        # create drawing # Default is 100%,100% - don't override that,
        # as this allows the svg to fit the data and expand as necessary
        self.plot = Drawing(filename, size=canvas_size)
        background = Rect(insert=(0, 0), size=canvas_size, fill="white")
        self.plot.add(background)

    def convert_xcoord_to_pos(self, xcoord):
        return round(float(xcoord - self.start) * self.scale_x, 2) + self.MARGIN

    def make_gausian(self, pos, height, stddev, horizontal=True, y_median=0, sigmas=3):
        """ path points will be at (-3stddev,0), (0,height), (3stddev,0)
            Control points at (-1stddev,0), (-1stddev,height), (1stddev,height), (1stddev,0)
         """
        x = [-sigmas * stddev, -1 * stddev, -1 * stddev, 0, stddev, stddev, sigmas * stddev]
        y = [0, 0, height, height, height, 0, 0]

        if horizontal is True:
            x = [round((x - self.start + pos) * self.scale_x, 2) + self.MARGIN for x in x]
            # Scale Y and inverse the coordinates
            y = [round(y1 * self.scale_y, 2) for y1 in y]
            y = [(self.height - self.BOTTOM_MARGIN - y2) for y2 in y]
        else:
            s = [round(((pos - self.start) * self.scale_x) + y + self.MARGIN + self.DISTR_SHIFT, 2) for y in y]
            y = [round(((x + y_median) * self.scale_y), 2) for x in x]
            x = s
        d = "M " + str(x[0]) + "," + str(y[0]) + " C"  # point 1
        for i in range(1, 7):
            d += " " + str(x[i]) + "," + str(y[i])
        return d

    @staticmethod
    def filter_waves(waves):
        i = 0
        while i < len(waves) - 1:
            if i > 0:  # check if wave is smaller than the last and should be removed
                a_pos, a_ht, a_sd = waves[i - 1]
                b_pos, b_ht, _b_sd = waves[i]
                if b_ht < a_ht and b_pos < a_pos + 3 * a_sd:
                    waves.pop(i)
                    continue
            if i < len(waves) - 2:  # check if wave is smaller than the next and should be removed
                a_pos, a_ht, _a_sd = waves[i]
                b_pos, b_ht, b_sd = waves[i + 1]
                if a_ht < b_ht and a_pos < b_pos - 3 * b_sd:
                    waves.pop(i)
                    continue
            i += 1

        return waves

    def save(self):
        """ push loaded elements to the the plot, clear out the elements. """
        for element in self.elements:
            self.plot.add(element)
        self.elements = None  # may want to remove this, if we ever want to do fancy stuff with the elements.
        self.plot.save()

    def to_string(self):
        """ convert the loaded elements to strings and return the list of elements"""
        magic_box = Text(" ", id="sample_name", insert=((self.MARGIN + 20), (self.MARGIN + 20)),
                         fill="black", font_size=medfont)
        self.elements.append(magic_box)

        t0 = time.time()
        temp = [self.plot.tostring().replace("</svg>", "")]
        for element in self.elements:
            temp.append(element.tostring())
        temp.append("</svg>")
        print(f" Conversion of SVG to string took {time.time() - t0} seconds")
        return ''.join(t for t in temp)

    def get_xml(self):
        """ Convert the loaded elements into XML strings and then return them."""
        strings = ""
        for element in self.elements:
            strings += (element.get_xml().decode('utf-8'))
        return strings

    def add_legends(self, get_cpg, annotations):
        """ Add annotations, title, axis, tic marks and labels """

        title = Text(self.title, insert=(bigfont + ((float(self.MARGIN) - bigfont) / 3),
                                         bigfont + ((float(self.MARGIN) - bigfont) / 3)),
                     fill=legend_color, font_size=bigfont)
        self.elements.append(title)

        for axis in get_axis(self.width, self.MARGIN, self.height, self.BOTTOM_MARGIN, self.RIGHT_MARGIN):
            self.elements.append(axis)

        # print("add_legends, messages are: {}".format(self.message)

        if self.message is None:
            self.add_xtics()
            # self.add_sample_labels(self.width - self.RIGHT_MARGIN + 20)
            if get_cpg:
                for cpg in add_cpg(annotations, self.MARGIN, self.height, self.scale_x, self.start, self.end,
                                   self.BOTTOM_MARGIN):
                    self.elements.insert(0, cpg)

    def add_xtics(self):
        """ Create X tics on the plot"""
        scale_tics = 1

        while scale_tics * 10 < self.end - self.start:
            scale_tics *= 10
        xtics = [i for i in range(self.start, self.end + 1) if i % scale_tics == 0]
        while len(xtics) < 4:
            scale_tics /= 2
            xtics += [j for j in range(self.start, self.end + 1) if j % scale_tics == 0 and j not in xtics]
        xtics.sort()
        spacing = fabs((self.MARGIN + (xtics[1] - self.start) * self.scale_x) -
                       (self.MARGIN + (xtics[0] - self.start) * self.scale_x)) / 4
        for tic in xtics:
            tic_x = (self.MARGIN + (tic - self.start) * self.scale_x)
            tic_y = self.height - self.BOTTOM_MARGIN + smallfont * 1.5
            ticmarker = (Text(str(tic), insert=(tic_x, tic_y), fill=legend_color, font_size=smallfont))
            ticline = Rect(insert=(tic_x, self.height - self.BOTTOM_MARGIN - 2), size=(1, 5), fill=legend_color)
            for i in range(1, 4):
                if tic_x - spacing * i > self.MARGIN - 5:
                    ticline2 = Rect(insert=(tic_x - spacing * i, self.height - self.BOTTOM_MARGIN - 2), size=(1, 2),
                                    fill=legend_color)
                    self.elements.append(ticline2)
            self.elements.append(ticline)
            self.elements.append(ticmarker)

    def add_ytics_chipseq(self):
        """ Add Y ticks to the svg plot """

        steps = round(self.maxh / 5, 1) if self.maxh else 1

        labels = [0, steps, 2 * steps, 3 * steps, 4 * steps, 5 * steps]
        ytics = [round(self.height - self.BOTTOM_MARGIN - (self.dimension_y / 5 * y), 3) for y in range(0, 6)]
        spacing = (ytics[0] - ytics[1]) / 2
        for tic, label in zip(ytics, labels):
            ticline = Rect(insert=(self.MARGIN - 2, tic), size=(5, 1), fill=legend_color)
            if tic - spacing > self.MARGIN:
                ticline2 = Rect(insert=(self.MARGIN - 2, tic - spacing), size=(2, 1), fill=legend_color)
                self.elements.append(ticline2)
            tic_x = self.MARGIN - smallfont * 2
            tic_y = tic + 1
            if len(str(label)) == 1:
                tic_x += 3
            if len(str(label)) == 2:
                tic_x += 2
            if len(str(label)) >= 3:
                tic_x -= 10
            ticmarker = (Text(str(label), insert=(tic_x, tic_y), fill=legend_color, font_size=smallfont))
            self.elements.append(ticline)
            self.elements.append(ticmarker)

    def add_ytics_methylation(self):
        """ Add Y ticks to the svg plot """
        labels = [0, 0.2, 0.4, 0.6, 0.8, 1]
        ytics = [round((self.MARGIN + self.dimension_y) - (y * self.dimension_y), 3) for y in labels]
        spacing = (ytics[0] - ytics[1]) / 2
        for tic, label in zip(ytics, labels):

            ticline = Rect(insert=(self.width - self.RIGHT_MARGIN, tic), size=(5, 1), fill=legend_color)
            if tic - spacing > self.MARGIN:
                ticline2 = Rect(insert=(self.width - self.RIGHT_MARGIN, tic - spacing), size=(2, 1), fill=legend_color)
                self.elements.append(ticline2)
            tic_x = self.width - self.RIGHT_MARGIN + smallfont
            tic_y = tic + 1
            if len(str(label)) == 1:
                tic_x += 3
            if len(str(label)) == 2:
                tic_x += 2
            ticmarker = (Text(str(label), insert=(tic_x, tic_y), fill=legend_color, font_size=smallfont))
            self.elements.append(ticline)
            self.elements.append(ticmarker)

    def draw_genes(self, genes):
        for gene in genes:
            for transcript in gene['transcripts']:

                start = self.convert_xcoord_to_pos(gene['start'])
                length = self.convert_xcoord_to_pos(gene['end']) - start
                if start < self.MARGIN:
                    if start < 0:  # first, remove anything before zero.
                        length += start
                        start = 0
                    length -= (self.MARGIN + start)  # then remove anything before the margin begins
                    start = self.MARGIN
                if start + length > (self.width - self.RIGHT_MARGIN):
                    length = (self.width - self.RIGHT_MARGIN) - start
                if gene['strand'] == 1:
                    text = gene['name'] + " ->>>"
                else:
                    text = " <<<- " + gene['name']
                # print "(self.width + self.RIGHT_MARGIN + self.MARGIN)", (self.width - self.RIGHT_MARGIN)
                # print "gene -> text:{} chrend:{} chrstart:{} start:{} length:{}"
                #       .format(gene['name'], gene['end'], gene['start'], start, length)_
                g = Rect(insert=(start, self.height - self.BOTTOM_MARGIN + self.gene_offset + 4),
                         size=(length, 2), fill="grey")
                t = (Text(text, insert=(start, self.height - self.BOTTOM_MARGIN + self.gene_offset + 9),
                          fill=legend_color, font_size=smallfont))
                self.elements.append(g)

                for exon in gene["transcripts"][transcript]["exons"]:
                    e = gene["transcripts"][transcript]["exons"][exon]
                    e_start = self.convert_xcoord_to_pos(e["start"])
                    e_len = self.convert_xcoord_to_pos(e['end']) - e_start
                    if e_start > (self.width - self.RIGHT_MARGIN) or (e_start + e_len) < self.MARGIN:
                        continue
                    if e_start < self.MARGIN:
                        e_start = self.MARGIN
                    if e_start + e_len > (self.width - self.RIGHT_MARGIN):
                        e_len = (self.width - self.RIGHT_MARGIN) - e_start

                    e = Rect(insert=(e_start, self.height - self.BOTTOM_MARGIN + self.gene_offset), size=(e_len, 9),
                             fill="grey")
                    self.elements.append(e)

                self.elements.append(t)
                self.gene_offset += 12
                if self.gene_offset > 250:
                    self.gene_offset = self.GENE_OFFSET
