from svgwrite.shapes import Rect

BIG_FONT = 20
MED_FONT = 14
SMALL_FONT = 10
LEGEND_COLOUR = 'black'

# pylint: disable=R0914


def get_axis(width, margin, height, bottom_margin, right_margin):
    """leave "margin" on either side of the image, draw the axes along the
    boundaries of the margin."""
    margin = margin
    height = height
    x_axis = Rect(insert=(margin, height - bottom_margin),
                  size=(width - (margin + right_margin), 1),
                  fill=LEGEND_COLOUR)
    y_axis = Rect(insert=(margin, margin),
                  size=(1, height - (margin + bottom_margin)),
                  # viewing area is the height, minus the top margin and bottom margin.
                  fill=LEGEND_COLOUR)
    y_axis2 = Rect(insert=(width - right_margin, margin),
                   size=(1, height - (margin + bottom_margin)),
                   # viewing area is the height, minus the top margin and bottom margin.
                   fill=LEGEND_COLOUR)
    return x_axis, y_axis, y_axis2


def add_cpg(annotations, margin, height, scale_x, start, end, bottom_margin):
    """draw the regions on the svg graph."""
    if annotations is None:
        return []
    elements = []

    color_high = 'darkseagreen'
    color_low = 'deepskyblue'
    for ((island_start, island_end), colour_type) in annotations['Islands']:
        if island_start < start:
            island_start = start
        if island_end > end:
            island_end = end
        x_position = margin + (island_start - start) * scale_x
        thickness = (island_end - island_start) * scale_x

        if 'IC' in colour_type:
            color = color_low
            opacity = 0.2
        elif 'HC' in colour_type:
            color = color_high
            opacity = 0.2
        else:
            color = 'white'
            opacity = 0
        island = Rect(insert=(x_position, margin),
                      size=(thickness, height - margin - bottom_margin),
                      fill=color,
                      fill_opacity=opacity)
        elements.append(island)

    return elements
