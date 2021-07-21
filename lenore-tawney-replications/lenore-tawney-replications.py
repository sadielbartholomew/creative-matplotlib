"""Replication of, and variations on, linear drawings by Lenore Tawney.

All six original drawings that are replicated were completed in 1964.

See also Tawney's website for information about the artist of the original
works:
  https://lenoretawney.org/

"""

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.patches import Polygon
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator


# See comments against first item for documentation of these design parameters
REPLICATION_DESIGN_PARAMETERS = {
    "The Great Breath": (
        # Coordinates of start and end points of all lines to draw.
        [
            ((9, 81), (80, 92)),
            ((80, 92), (150, 81)),
            ((10, 15), (80, 6)),
            ((80, 6), (150, 15)),
            ((10, 40), (80, 6)),
            ((80, 6), (150, 40)),
        ],
        # All pairs of lines, identified by (zero-indexed) position in above
        # line coordinates listing, to be joined together with many lines from
        # points equally-spaced and sequentially drawn across both lines.
        [(0, 3), (1, 2), (1, 4), (0, 5)],
        # Design style, three-tuple of:
        #   1. figsize, scaling_factor;
        #   2. of lines: line width, line alpha, wiggliness (via rcparams);
        #   3. colours: background colour, grid colour, line colour.
        #   4. (optional) change to the number of lines to draw between coors
        (
            ((11, 6.75), 100),
            (0.4, 0.6, False),
            ("#E7DACB", "#9EC3EA", "#2F1E1E"),
        ),
        # Optional dict to override colour for given coor pair (by index).
        {},
        # Optional list to plot a regular polygon, as required for some designs
        # where the 6-tuple gives:
        # (number of sides, centre position, radius, rotational factor, colour,
        # optional Bool for whether or not to plot lines across assumed False)
        [],
    ),
    "Wings of the Wind": (
        [
            ((25, 50), (105, 25)),
            ((105, 25), (185, 50)),
            ((25, 129), (105, 121)),
            ((105, 121), (185, 129)),
        ],
        [(0, 3), (1, 2)],
        (
            ((8, 6), 160),
            (0.35, 0.7, False),
            ("#E6DFD5", "#BCB9A9", "#37272A"),
        ),
    ),
    "From Its Center": (
        [
            ((5, 15), (65, 15)),
            ((5, 75), (35, 95)),
            ((35, 95), (65, 75)),
        ],
        [
            (0, 1),
            (0, 2),
        ],
        (
            ((4, 5.75), 70),  # 10 up by 7 across
            (0.5, 1.0, False),
            ("#F7F3F0", "#1C1815", "#030000"),
        ),
    ),
    "Union of Water and Fire II": (
        [
            ((20, 130), (140, 130)),
            ((20, 70), (140, 70)),
        ],
        [((80, 40), 0), ((80, 160), 1)],
        (
            ((5, 6.25), 160),  # 20 by 16 (TODO: thicker half grid lines too)
            (0.5, 0.4, False),
            ("#E8E3DD", "#E0A66C", "#464476"),
            100,
        ),
        {1: "#E75136"},
    ),
    "The Eternal Band": (
        [
            ((60, 60), (60.26126851, 99.99914673)),
            ((60, 60), (28.89030607, 85.14332801)),
            ((60, 60), (20.94557768, 51.35407047)),
            ((60, 60), (42.40962587, 24.07537421)),
            ((60, 60), (77.11958455, 23.8486539)),
            ((60, 60), (98.93814689, 50.84463455)),
            ((60, 60), (91.43549043, 84.73479212)),
        ],
        [
            # 6, 0 -> 5 and not 1 -> 6, 0 to give join lines pointing clockwise
            ((60.26126851, 99.99914673), 6),
            ((28.89030607, 85.14332801), 0),
            ((20.94557768, 51.35407047), 1),
            ((42.40962587, 24.07537421), 2),
            ((77.11958455, 23.8486539), 3),
            ((98.93814689, 50.84463455), 4),
            ((91.43549043, 84.73479212), 5),
        ],
        (
            ((8, 8), 120),  # 20 by 16 (TODO: thicker half grid lines too)
            (0.5, 0.7, False),
            # Fake having no gridlines by plotting in background colour!
            ("#ECEDEF", "#ECEDEF", "#C8431E"),
            30,
        ),
        {},
        # First polygon approximates a circle with high enough N of sides
        [
            (1000, (60, 60), 40, 1, "#C8431E"),
            # Use Pythagoras' theorem to have square sides tangential to circle
            (4, (60, 60), np.sqrt(2 * 40 ** 2), 4, "#827876"),
            # Don't plot this, but the following was uncommented and printed
            # out later in the code to get the points for the design:
            # (7, (60, 60), 40, 1.5 * np.pi, "#1B1818"),  # to print for points
        ],
    ),
    "Blue Circle": (
        [
            ((195, 80), (585, 80)),
            ((195, 470), (585, 470)),
            ((195, 80), (195, 470)),
            ((585, 80), (585, 470)),
        ],
        [(0, 1), (2, 3)],
        (
            ((8.5, 6), 550),
            (0.5, 0.6, False),
            ("#E1D9CC", "#B4AD9D", "#2D2306"),
            120,
        ),
        {},
        [
            # Approximates a circle with high enough N of sides but here the
            # N approximation is also the number of lines used to join circle
            (4 * 120, (390, 275), 70, 1, "#2541C1", True),
        ],
    ),
}

VARIATION_DESIGN_PARAMETERS = {}


def plot_line_segment(
    startpoint_coors, endpoint_coors, colour, linewidth, alpha=1.0
):
    """TODO."""
    plt.plot(
        [startpoint_coors[0], endpoint_coors[0]],
        [startpoint_coors[1], endpoint_coors[1]],
        color=colour,
        linewidth=linewidth,
        alpha=alpha,
    )


def plot_straight_line_by_equation(gradient, intercept, colour, linewidth):
    """TODO."""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + gradient * x_vals
    plt.plot(x_vals, y_vals, color=colour, linewidth=linewidth)


def draw_between_line_segments(
    line_seg_1,
    line_seg_2,
    colour,
    linewidth,
    number_lines_to_draw=68,
    alpha=1.0,
):
    """TODO."""
    xs = np.linspace(line_seg_1[0], line_seg_1[1], num=number_lines_to_draw)
    ys = np.linspace(line_seg_2[1], line_seg_2[0], num=number_lines_to_draw)
    for x, y in zip(xs, ys):
        plot_line_segment(
            x, y, colour=colour, linewidth=linewidth, alpha=alpha
        )


def draw_from_point_to_line_segment(
    point, line_seg, colour, linewidth, number_lines_to_draw=68, alpha=1.0
):
    """TODO."""
    ys = np.linspace(line_seg[0], line_seg[1], num=number_lines_to_draw)
    for y in ys:
        plot_line_segment(
            point, y, colour=colour, linewidth=linewidth, alpha=alpha
        )


def draw_regular_polygon(
    number_sides, centre, radius, rotation_no, colour, lw, alpha, ax
):
    """TODO."""
    # First get the vertex coordinates
    polygon_coors = []
    # Taken and adapted from some code in the 'repolygon' project of this repo
    for vertex in range(1, number_sides + 2):
        factor = 2 * vertex * np.pi / number_sides + np.pi / rotation_no
        # Note: radius == repolygon scale
        polygon_coors.append(
            radius * np.array([np.cos(factor), np.sin(factor)])
            + np.array(centre)
        )

    # Now draw those vertices forming the regular polygon
    polygon = Polygon(
        polygon_coors, fill=False, edgecolor=colour, linewidth=lw, alpha=alpha
    )
    ax.add_patch(polygon)

    # Use this to get the points required for replication The Eternal Band
    # if number_sides == 7:  # to find the heptagon vertices for The Eternal Band
    #    print("Centre is at:", centre)
    #    print("Vertices are at:", polygon_coors)

    return polygon_coors


def draw_across_regular_polygon(
    polygon_centre, polygon_coors, colour, lw, alpha, ax
):
    """TODO."""
    # Note: if polygon is an approximated circle, must approximate circle
    # with the effective number of lines to draw divided by two to get the
    # desired spacing.

    # First strip the final coor. which is the first one duplicated:
    polygon_coors = polygon_coors[:-1]

    # Draw from the centre out to the vertices of the polygon:
    for c in polygon_coors:
        plot_line_segment(
            polygon_centre, c, colour=colour, linewidth=lw, alpha=alpha
        )


def format_grids(ax, grid_colour):
    """TODO."""
    ax.set_axisbelow(True)
    ax.minorticks_on()

    # Set the spacings:
    # Major dividers every 10 points, minor every 1, on the given axis
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Customize the grids
    ax.grid(
        which="major",
        linestyle="-",
        linewidth=0.8,
        color=grid_colour,
        alpha=0.5,
    )
    ax.grid(
        which="minor",
        linestyle="-",
        linewidth=0.5,
        color=grid_colour,
        alpha=0.3,
    )


def pre_format_plot(
    figsize, scale_factor, sketch_params, background_colour, grid_colour
):
    """TODO."""
    # Configure very slightly squiggly lines for a more 'hand-drawn' look!
    # This doesn't seem possible at the moment (without making the code much
    # less clean, at least) for the drawn lines only, it also affects the axes and
    # gridlines etc., but is fun to play around with these parameters to see how
    # it influences the style! Note that the 'xkcd' style uses (1, 100, 2): see
    # https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/pyplot.py
    if sketch_params:
        rcParams["path.sketch"] = sketch_params

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(background_colour)

    # Scale plot limits with figsize so the grid ends up composed of squares:
    if figsize[0] < figsize[1]:
        plot_limits_x = (0, scale_factor)
        plot_limits_y = (0, plot_limits_x[1] * figsize[1] / figsize[0])
    else:
        plot_limits_y = (0, scale_factor)
        plot_limits_x = (0, plot_limits_y[1] * figsize[0] / figsize[1])

    ax.set_xlim(plot_limits_x)
    ax.set_ylim(plot_limits_y)

    format_grids(ax, grid_colour)

    return fig, ax


def post_format_plot(ax, background_colour, view_axes_labels_as_guide=False):
    """TODO."""
    ax.set_facecolor(background_colour)

    # Whilst creating a design, we may want to see the axes labels
    if view_axes_labels_as_guide:
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
    else:
        # Note can't just use ax.axis("off") as it hides the grid too
        for ax_choice in ("x", "y"):
            plt.tick_params(
                axis=ax_choice,
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
                labeltop=False,
                labelleft=False,
                labelright=False,
            )
        ax.set_frame_on(False)
    plt.tight_layout()


def plot_overall_design(
    design_to_draw, output_name, view_axes_labels_as_guide=False
):
    """TODO."""
    # Unpack geometrical parameters
    line_coors, coor_pairs_to_join = design_to_draw[:2]
    # Unpack style parameters
    dims, line_params, colour_params, *num_lines_to_draw = design_to_draw[2]

    figsize, scale_factor = dims
    linewidth, line_alpha, sketch_rcparams = line_params
    background_colour, grid_colour, default_line_colour = colour_params

    fig, ax = pre_format_plot(
        figsize, scale_factor, sketch_rcparams, background_colour, grid_colour
    )

    # Get change of colours for given pairs of coors to join, if specified:
    change_of_colour = {}
    if len(design_to_draw) >= 4:
        change_of_colour = design_to_draw[3]
    # Get any optional polygons to draw and then draw them first
    if len(design_to_draw) == 5:
        polygons_to_draw = design_to_draw[4]

        join_across = False  # default

        for polygon in polygons_to_draw:
            if len(polygon) > 5:
                join_across = polygon[5]
                polygon = polygon[:5]

            if join_across:
                coors = draw_regular_polygon(
                    *polygon, linewidth, line_alpha, ax
                )
                # where, as specified below, index 1 is centre and 4 is colour
                draw_across_regular_polygon(
                    polygon[1], coors, polygon[4], linewidth, line_alpha, ax
                )
            else:
                # Plot with same line width and alpha as rest of the design
                draw_regular_polygon(*polygon, linewidth, line_alpha, ax)

    # Plot the lines comprising the design
    for index, line_coor in enumerate(line_coors):
        colour = default_line_colour
        if index in change_of_colour.keys():
            colour = change_of_colour[index]

        plot_line_segment(*line_coor, colour, linewidth, line_alpha)

    # Drawing of equally-spaced lines between given pairs of segments
    for index, pairs in enumerate(coor_pairs_to_join):
        coor_1, coor_2 = pairs

        colour = default_line_colour
        if index in change_of_colour.keys():
            colour = change_of_colour[index]
        kwargs = {"alpha": line_alpha}
        if num_lines_to_draw:
            kwargs["number_lines_to_draw"] = num_lines_to_draw[0]

        if isinstance(coor_1, tuple):  # not a line but a single given point
            draw_from_point_to_line_segment(
                coor_1, line_coors[coor_2], colour, linewidth, **kwargs
            )
        else:
            draw_between_line_segments(
                line_coors[coor_1],
                line_coors[coor_2],
                colour,
                linewidth,
                **kwargs,
            )

    post_format_plot(
        ax,
        background_colour,
        view_axes_labels_as_guide=view_axes_labels_as_guide,
    )
    plt.savefig(
        f"img/replications/{output_name}.png",
        format="png",
        bbox_inches="tight",
        dpi=1000,
    )
    plt.show()


# Plot all replication designs (separately)
for name in [
    "From Its Center",
    "The Great Breath",
    "Wings of the Wind",
    "Union of Water and Fire II",
    "The Eternal Band",
    "Blue Circle",
]:
    design_to_draw = REPLICATION_DESIGN_PARAMETERS[name]
    plot_overall_design(
        design_to_draw,
        name.replace(" ", "_").lower(),
        # view_axes_labels_as_guide=True
    )
