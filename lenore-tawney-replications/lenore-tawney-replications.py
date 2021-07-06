"""Replication of, and variations on, linear drawings by Lenore Tawney.

All six original drawings that are replicated were completed in 1964.

See also Tawney's website for information about the artist of the original
works:
  https://lenoretawney.org/

"""

import numpy as np

from matplotlib import rcParams
import matplotlib.pyplot as plt
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
        (
            ((11, 6.75), 100),
            (0.4, 0.6, False),
            ("#E7DACB", "#9EC3EA", "#2F1E1E"),
        ),
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
        [],
        [],
        (
            (),
            (),
            (),
        ),
    ),
    "Blue Circle": (
        [],
        [],
        (
            (),
            (),
            (),
        ),
    ),
    "The Eternal Band": (
        [],
        [],
        (
            (),
            (),
            (),
        ),
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
    number_lines_to_draw=50,
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
    point, line_seg, colour, linewidth, number_lines_to_draw=50, alpha=1.0
):
    """TODO."""
    ys = np.linspace(line_seg[0], line_seg[1], num=number_lines_to_draw)
    for y in ys:
        plot_line_segment(
            point, y, colour=colour, linewidth=linewidth, alpha=alpha
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
    dims, line_params, colour_params = design_to_draw[2]
    figsize, scale_factor = dims
    linewidth, line_alpha, sketch_rcparams = line_params
    background_colour, grid_colour, default_line_colour = colour_params

    fig, ax = pre_format_plot(
        figsize, scale_factor, sketch_rcparams, background_colour, grid_colour
    )

    # Plot the lines comprising the design
    for line_coor in line_coors:
        plot_line_segment(
            *line_coor, default_line_colour, linewidth, line_alpha
        )

    # Drawing of equally-spaced lines between given pairs of segments
    for pairs in coor_pairs_to_join:
        index_1, index_y = pairs
        draw_between_line_segments(
            line_coors[index_1],
            line_coors[index_y],
            default_line_colour,
            linewidth,
            68,
            alpha=line_alpha,
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
]:
    design_to_draw = REPLICATION_DESIGN_PARAMETERS[name]
    plot_overall_design(design_to_draw, name.replace(" ", "_").lower())
