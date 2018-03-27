
from svgwrite.shapes import Line, Circle
from svgwrite.text import Text
from SVG.base_figure import Figure

INIT_GAP = 3


class ScoringGraphic(Figure):

    def __init__(self, show_legend, width=800, height=600, debug=False, x_min=None, x_max=None, y_min=0,
                 y_max=0, margin_top=20, margin_bottom=40, margin_left=20, margin_right=20):
        Figure.__init__(self, width=width,
                        height=height,
                        margin_top=margin_top,
                        x_max=x_max,
                        y_max=y_max,
                        x_min=x_min,
                        y_min=y_min,
                        margin_bottom=margin_bottom,
                        margin_left=margin_left,
                        margin_right=margin_right,
                        debug=debug)

        self.show_legend = show_legend

        self.annotated_scores = None
        self.max_value = None
        self.min_value = None

    def add_annotated_scores(self, annotated_scores):
        print(f"{annotated_scores}")
        self.annotated_scores = annotated_scores

    @staticmethod
    def print_data(annotated_scores):
        for sample, details in annotated_scores.items():
            print(f"{sample}\t{details['score']}\t"
                  f"{details['type'] if 'type' in details else ''}\t"
                  f"{details['category'] if 'category' in details else ''}")

    def plot_data(self):
        if not self.show_legend:
            self.plot.add(Line(start=(self.margin_left, self.margin_top),
                          end=(self.width-self.margin_right, self.margin_top),
                          stroke_width=1, stroke="black"))

        self.max_value = max([x['score'] for x in self.annotated_scores.values()])
        if not self.min_value:
            self.min_value = min([x['score'] for x in self.annotated_scores.values()])

        if not self.show_legend:
            self.plot.add(Text("Fibroblasts",
                          insert=(self.margin_left, self.margin_top-5),
                          fill="black", font_size="15"))
            self.plot.add(Text("Cardiomyocytes",
                          insert=(self.width-self.margin_right-100, self.margin_top-5),
                          fill="black", font_size="15"))

        delta = self.max_value - self.min_value
        plottable = self.width - (self.margin_left + self.margin_right)

        n = {"Fibroblasts": INIT_GAP,
             "Cardiomyocytes": INIT_GAP,
             "Experimental": INIT_GAP,
             "other": INIT_GAP}

        for sample, sample_details in self.annotated_scores.items():

            position = self.margin_left + ((sample_details['score'] - self.min_value)/delta * plottable)
            # colour = "grey"
            if "category" in sample_details:
                sample_type = sample_details["category"]
                if sample_type == "Fibroblasts":
                    colour = "green"
                elif sample_type == "Cardiomyocytes":
                    colour = "blue"
                elif sample_type == "Experimental":
                    colour = "red"
                else:
                    continue
                    # sample_type = "other"
            else:
                continue
                # sample_type = "other"

            c = Circle(center=(position, self.margin_top + n[sample_type] + 5),
                       r=3,
                       stroke_width=0.1,
                       stroke_linecap='round',
                       stroke_opacity=1,
                       fill=colour,
                       fill_opacity=0.6)  # set to 0.2 if you want to show clear.
            c.set_desc('{} - {} - {}'.format(sample, sample_type,
                                             sample_details["score"] if "description" not in sample_details
                                             else sample_details["description"]))
            self.plot.add(c)
            if sample_type == "other":
                n[sample_type] += 3
            else:
                n[sample_type] += 6

    def save(self, reset=True):
        super().save(reset)

    def set_filename(self, filename):
        super().set_filename(filename)
