"""Replication of, and variations on, linear drawings by Lenore Tawney.

See also Tawney's website for information about the artist of the original
works:
  https://lenoretawney.org/

"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


BACKGROUND_COLOUR = "#FBF4EA"  # beige colour taken from photo of an original
GRID_COLOUR = "powderblue"
DEFAULT_LINE_COLOUR = "#1D1616"  # off-black, very dark grey for better effect
LINEWIDTH = 0.5

FIGSIZE = (11, 6.75)  # like landscape A4 (graph-gridded) paper

# Scale plot limits with the figsize so the grid ends up composed of squares:
if FIGSIZE[0] < FIGSIZE[1]:
    plot_limits_x = (0, 100)
    plot_limits_y = (0, plot_limits_x[1] * FIGSIZE[1] / FIGSIZE[0])
else:
    plot_limits_y = (0, 100)
    plot_limits_x = (0, plot_limits_y[1] * FIGSIZE[0] / FIGSIZE[1])


def plot_line_segment(
    startpoint_coors, endpoint_coors, colour=DEFAULT_LINE_COLOUR
):
    """TODO."""
    plt.plot(
        [startpoint_coors[0], endpoint_coors[0]],
        [startpoint_coors[1], endpoint_coors[1]],
        color=colour,
        linewidth=LINEWIDTH,
    )


def plot_straight_line_by_equation(
    gradient, intercept, colour=DEFAULT_LINE_COLOUR
):
    """TODO."""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + gradient * x_vals
    plt.plot(x_vals, y_vals, color=colour, linewidth=LINEWIDTH)


def draw_between_line_segments(
    line_seg_1,
    line_seg_2,
    number_lines_to_draw=50,
    colour=DEFAULT_LINE_COLOUR,
):
    """TODO."""
    xs = np.linspace(line_seg_1[0], line_seg_1[1], num=number_lines_to_draw)
    ys = np.linspace(line_seg_2[1], line_seg_2[0], num=number_lines_to_draw)
    for x, y in zip(xs, ys):
        print(x, y)
        plot_line_segment(x, y, colour=colour)


def draw_from_point_to_line_segment(
    point,
    line_seg,
    number_lines_to_draw=50,
    colour=DEFAULT_LINE_COLOUR,
):
    """TODO."""
    ys = np.linspace(line_seg[0], line_seg[1], num=number_lines_to_draw)
    for y in ys:
        plot_line_segment(point, y, colour=colour)


def format_grids(ax):
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
        color=GRID_COLOUR,
        alpha=0.5,
    )
    ax.grid(
        which="minor",
        linestyle="-",
        linewidth=0.5,
        color=GRID_COLOUR,
        alpha=0.3,
    )


def pre_format_plot():
    """TODO."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.set_facecolor(BACKGROUND_COLOUR)

    ax.set_xlim(plot_limits_x)
    ax.set_ylim(plot_limits_y)

    format_grids(ax)

    return fig, ax


def post_format_plot(ax, view_axes_labels_as_guide=False):
    """TODO."""
    ax.set_facecolor(BACKGROUND_COLOUR)

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


def plot_overall_design(line_coors, view_axes_labels_as_guide=False):
    """TODO."""
    fig, ax = pre_format_plot()

    # Plot the lines comprising the design
    for line_coor in line_coors:
        plot_line_segment(*line_coor)

    # Test a drawing of equally-spaced lines between two segments
    draw_between_line_segments(line_coors[0], line_coors[3], 75)
    draw_between_line_segments(line_coors[1], line_coors[2], 75)
    draw_from_point_to_line_segment((0, 0), line_coors[0], colour="indianred")

    post_format_plot(ax, view_axes_labels_as_guide=view_axes_labels_as_guide)
    plt.show()


# Plot
line_coors = [
    ((9, 81), (80, 92)),  # 1, join to 4
    ((80, 92), (150, 80)),  # 2, join to 3
    ((9, 15), (80, 6)),  # 3, join to 2
    ((80, 6), (150, 15)),  # 4, join to 1
]
plot_overall_design(line_coors, view_axes_labels_as_guide=True)
