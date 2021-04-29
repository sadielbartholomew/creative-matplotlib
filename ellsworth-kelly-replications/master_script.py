"""
Replication of selected artworks by Ellsworth Kelly with NumPy arrays.

Created by Sadie Bartholomew, 2019.

    ***
    TODO for this mini-project:

    * refactor to make data procesing code less coupled;
    * fix minor bug where grid-lines as square borders e.g. for S1_DESIGN
      are not exactly aligned with the edges of the squares;
    * fix another minor bug whereby there are small gaps at corners in any
      borders due to their creation by offset on spines;
    * to make the images look less artificial:
       * utilise a function to apply a slight random variation in colour for
         each square plotted associated with each colour in the scheme;
       * effective hinton diagram to make squares vary slightly in size: see
         https://matplotlib.org/examples/specialty_plots/hinton_demo.html.
    ***

"""


from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np


# 'Nine Squares', source: tate.org.uk/art/artworks/kelly-nine-squares-p77435
#
# Tuple items are, in order:
#   1. configuration parameters;
#   2. the background colour, in R,G,B Decimal Code (3-tuple of ints 0-255);
#   3. the other colours used in the design, also in R,G,B Decimal Code.
#      Note: the order of these matters for the plotting logic, so we rely
#      on the dictionary ordering property for iteration of Python 3.
NS_DESIGN = (
    (3, 10, 6, 5.0),
    (242, 233, 234),
    {
        "NS_GREEN": (57, 121, 87),
        "NS_YELLOW": (253, 214, 49),
        "NS_BLUE": (22, 32, 91),
        "NS_LIGHTBLUE": (81, 123, 197),
        "NS_BLACK": (28, 26, 29),
        "NS_ORANGE": (198, 85, 43),
        "NS_LIGHTORANGE": (231, 132, 5),
        "NS_LIGHTGREEN": (165, 192, 141),
        "NS_PURPLE": (77, 50, 105),
    },
)

# 'Spectrum I', source: ellsworthkelly.org/work/spectrum-i/
#
# The tuple has only one item, the design colours, in R,G,B Decimal Code.
# Note: there is no background hence no designated background colour, &
# as in the NS design above, the order of colours matters i.e. we rely
# on Python 3 dict ordering.
S1_DESIGN = {
    "S1_YELLOW": (253, 226, 24),
    "S1_LIGHTGREEN": (89, 172, 80),
    "S1_GREEN": (1, 146, 59),
    "S1_TEAL": (1, 124, 104),
    "S1_LIGHTERBLUE": (1, 105, 166),
    "S1_BLUE": (46, 85, 162),
    "S1_PURPLE": (110, 66, 133),
    "S1_PUCE": (156, 70, 107),
    "S1_MAGENTA": (184, 49, 82),
    "S1_RED": (222, 38, 47),
    "S1_ORANGE": (231, 71, 45),
    "S1_LIGHTERORANGE": (236, 112, 52),
    "S1_DARKYELLOW": (247, 171, 25),
}

# SCABC 2 and 4 use many similar colours to e/o, so share definitions:
SCABCX_COLOURS = {
    "SCABCX_YELLOW": (223, 196, 84),
    "SCABCX_TERRACOTTA": (160, 50, 46),
    "SCABCX_LIGHTTERRACOTTA": (182, 76, 56),
    "SCABCX_ORANGE": (221, 137, 60),
    "SCABCX_SAND": (211, 156, 83),
    "SCABCX_BROWN": (123, 86, 59),
    "SCABCX_BEIGE": (220, 167, 146),
    "SCABCX_PLUM": (136, 66, 101),
    "SCABCX_LILAC": (190, 170, 181),
    "SCABCX_PALEGREEN": (181, 188, 131),
    "SCABCX_LIGHTGREEN": (147, 179, 96),
    "SCABCX_LIGHTBLUE": (112, 168, 201),
}
# Unique colours for SCABCX designs to add the above for each case:
SCABC2_UNIQUE = {
    "SCABC2_DARKGREYBLUE": (64, 68, 84),
    "SCABC2_BLACK": (49, 46, 42),  # lighter black than for SCABC4
    "SCABC2_BLUE": (69, 87, 162),
    "SCABC2_GREEN": (120, 137, 112),
}
SCABC4_UNIQUE = {
    "SCABC4_LIGHTERBLUE": (26, 67, 150),
    "SCABC4_BLUE": (27, 47, 115),
    "SCABC4_NAVYBLUE": (2, 54, 97),
    "SCABC4_BRIGHTORANGE": (206, 90, 23),
    "SCABC4_GREEN": (37, 106, 85),
}

# Data for all 'by chance' works in the same form for processing
BY_CHANCE_SHARED_PLOTTING_CONFIG = (2, 9, 0.05)
BY_CHANCE_DESIGNS = {
    # 'Colors for a Large Wall',
    #     source: ellsworthkelly.org/work/colors-for-a-large-wall/
    "CFALW": (
        (8, 0.15, 0.05),
        (0.0, True),  # border and internal squares border ("grid")
        (245, 245, 245),
        {
            "CFALW_BLACK": (8, 4, 3),
            "CFALW_BROWN": (60, 10, 12),
            "CFALW_PURPLE": (73, 34, 98),
            "CFALW_LILAC": (176, 141, 185),
            "CFALW_PINK": (238, 126, 138),
            "CFALW_BLUE": (19, 71, 152),
            "CFALW_LIGHTBLUE": (13, 147, 208),
            "CFALW_DARKBLUE": (2, 39, 84),
            "CFALW_GREEN": (1, 80, 80),
            "CFALW_LIGHTGREEN": (156, 192, 164),
            "CFALW_YELLOW": (254, 218, 35),
            "CFALW_LIGHTORANGE": (242, 133, 2),
            "CFALW_RED": (230, 54, 30),
        },
    ),
    # 'Spectrum Colors Arranged by Chance II',
    #     source: moma.org/collection/works/37202
    "SCABC2": (
        (38, 0.48, 0.2),
        (3.0, False),
        (233, 227, 213),
        {**SCABCX_COLOURS, **SCABC2_UNIQUE},
    ),
    # 'Spectrum Colors Arranged by Chance IV',
    #     source: ellsworthkelly.org/work/spectrum-colors-arranged-by-chance/
    "SCABC4": (
        (38, 0.48, 0.2),
        (3.0, False),
        (8, 11, 11),
        {**SCABCX_COLOURS, **SCABC4_UNIQUE},
    ),
    # 'Spectrum Colors Arranged by Chance VII',
    #     source: ellsworthkelly.org/work/spectrum-colors-arranged-by-chance/
    "SCABC7": (
        (40, 0.0, 0.0),
        (0.0, False),
        (223, 200, 19),  # no background as such here, so just use BRIGHTYELLOW
        {
            "SCABC7_DARKTEAL": (0, 56, 82),
            "SCABC7_DULLYELLOW": (231, 184, 71),
            "SCABC7_LIGHTORANGE": (241, 153, 0),
            "SCABC7_ORANGE": (214, 79, 8),
            "SCABC7_BROWN": (157, 31, 7),
            "SCABC7_RED": (226, 50, 21),
            "SCABC7_PINK": (241, 148, 156),
            "SCABC7_PURPLE": (78, 17, 81),
            "SCABC7_PLUM": (97, 21, 58),
            "SCABC7_GREYLILAC": (197, 183, 198),
            "SCABC7_LIMEGREEN": (175, 192, 38),
            "SCABC7_LIGHTGREEN": (140, 193, 115),
            "SCABC7_GREEN": (0, 149, 101),
            "SCABC7_BRIGHTBLUE": (46, 174, 208),
            "SCABC7_LIGHTBLUE": (76, 145, 176),
            "SCABC7_BLUE": (15, 64, 141),
            "SCABC7_DARKBLUE": (33, 45, 122),
        },
    ),
}


def convert_rgb_tuple(tuple_256):
    """Convert R,G,B Decimal Code from 8-bit integers to [0, 1] floats.

    E.g. (255, 247, 0) -> (1., 0.9686... , 0.) representing
    a specific yellow colour, namely #FFF700 in Hex(ademical).
    """
    return tuple(float(rgb_int) / 255 for rgb_int in tuple_256)


def set_colours(colours_dict, background_colour=False):
    """Create a discrete custom colour map of all design colours."""
    # Force background by making it first in list:
    all_colours = list(colours_dict.values())
    if background_colour:
        all_colours.insert(0, background_colour)
    ns_cmap = [convert_rgb_tuple(rgb) for rgb in all_colours]
    return ListedColormap(ns_cmap)


def format_axes(ax, border_params, border_on_sqs_extent=None):
    """Customise the graphical decoration aspects for a given subplot.

    Notably hide the ticks and tick labels so it looks like a canvas
    rather than a grphical plot. Optionally add a border and/or some
    subtle lines separating each square plotted within the subplot.
    """
    ax.set_aspect("equal")
    # Hide labels and ticks but keep grid viewable if desired (border_on_sqs):
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.xaxis.set_ticks_position("none")
    ax.yaxis.set_ticks_position("none")
    if border_params:  # adds a border to each whole subplot
        border_width, border_colour = border_params
        for spine in ax.spines.values():  # use the spines as effective border
            spine.set_linewidth(border_width)
            spine.set_color(border_colour)
            # This offset makes the spine-based border just touch the design
            # edges, without overlapping any of the design:
            spine.set_position(("outward", border_width / 2))
    # This block must come after the above or the styling will be overwritten:
    if border_on_sqs_extent:  # adds subtle lines between each plotted square
        squares_array = np.arange(-0.5, border_on_sqs_extent, 1.0)
        # Shift gridlines from centre of each square to edges:
        ax.set_xticks(squares_array)
        ax.set_yticks(squares_array)
        ax.xaxis.grid(which="major", color="darkgrey", alpha=0.4)
        ax.yaxis.grid(which="major", color="darkgrey", alpha=0.4)


def plot_one_image(name, image, cmap, border_params=False):
    """Create a formatted figure with a single plot in given colourmap."""
    if not border_params:  # the default is no border (including no spines)
        border_params = (0.0, "white")
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=cmap)
    format_axes(ax, border_params)
    plt.savefig(
        "img/%s.png" % name, format="png", bbox_inches="tight", dpi=1000
    )
    plt.show()


def plot_NS(ns_data):
    """Plot the replication of the 'Nine Squares' piece."""
    # Unpack required data:
    ns_parameters, ns_backgr, ns_colours = ns_data
    no_squares, sq_len, square_spacing, border_width = ns_parameters

    # Create array representing the 'grid' structure of the design:
    size = 3 * sq_len + 2 * square_spacing
    image = np.zeros((size, size))

    indiv_square = np.ones((sq_len, sq_len))
    range_args = (
        0,
        sq_len * no_squares + 2 * square_spacing,
        sq_len + square_spacing,
    )
    for pos_i in range(*range_args):
        for pos_j in range(*range_args):
            image[
                pos_i : sq_len + pos_i, pos_j : sq_len + pos_j
            ] = indiv_square
            indiv_square += 1.0  # increments *all* elements in the array

    # Map colours to data values in order. Note: relies on Py3 dict ordering:
    border_p = (border_width, convert_rgb_tuple(ns_backgr))
    plot_one_image("NS", image, set_colours(ns_colours, ns_backgr), border_p)


def plot_S1(s1_data):
    """Plot the replication of the 'Spectrum I' piece."""
    # Create array representing the 'striped' structure of the design:
    size = len(s1_data.keys()) + 1  # +1 as two columns have same colour
    image_flat_data = np.array(list(range(size)) * size)
    image = image_flat_data.reshape(size, size)  # [0, 1, 2...] for all rows
    image[:, size - 1] = 0  # make final column same value (colour) as first

    # Map colours to data values in order. Note: relies on Py3 dict ordering:
    plot_one_image("S1", image, set_colours(s1_data), False)


def create_by_chance_image(tuning_params, backgr_colour, colours):
    """Use random sampling to create a 'by chance' design image array."""
    # Unpack the data defining each invididual design:
    squares_per_side, circularity_param, offset_param = tuning_params

    image = np.random.uniform(size=(squares_per_side, squares_per_side))
    # Make outer squares more often background, otherwise it is just an array
    # of random colours:
    for i in range(squares_per_side):
        for j in range(squares_per_side):
            centre_dist = (
                (squares_per_side / 2 - i) ** 2
                + (squares_per_side / 2 - j) ** 2
            ) ** circularity_param
            centre_prob = 2 * centre_dist / squares_per_side - offset_param
            if np.random.random_sample() < centre_prob:
                image[i, j] = 0.0
    return (image, set_colours(colours, backgr_colour))


def plot_by_chance(design_choice, plot_four_subplots=True):
    """Plot the generated replications of the chosen 'by chance' pieces."""
    # Unpack data:
    tuning, border_grid, backgr_col, col = BY_CHANCE_DESIGNS[design_choice]
    border_width, grid_on = border_grid
    if plot_four_subplots:
        plots_per_side, size, spacing = BY_CHANCE_SHARED_PLOTTING_CONFIG
        # Force figure to be square with a 4x4 grid of very close subplots:
        fig, ax = plt.subplots(
            plots_per_side, plots_per_side, figsize=(size, size)
        )
        plt.subplots_adjust(wspace=spacing, hspace=spacing)
        for i in range(plots_per_side):
            for j in range(plots_per_side):
                ax[i, j].imshow(
                    *create_by_chance_image(tuning, backgr_col, col)
                )
                border_on_extent = None
                if grid_on:
                    border_on_extent = tuning[0]  # the squares per side
                args = (
                    ax[i, j],
                    (border_width, convert_rgb_tuple(backgr_col)),
                )
                format_axes(*args, border_on_sqs_extent=border_on_extent)
        plt.savefig(
            "img/%s.png" % design_choice,
            format="png",
            bbox_inches="tight",
            dpi=1000,
        )
        plt.show()
    else:
        plot_one_image(
            design_choice, *create_by_chance_image(tuning, backgr_col, col)
        )


# Run functions on the relevant data to plot all defined designs:
plot_NS(NS_DESIGN)
plot_S1(S1_DESIGN)
for design in BY_CHANCE_DESIGNS.keys():
    plot_by_chance(design)
