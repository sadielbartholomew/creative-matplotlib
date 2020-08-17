import itertools

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import numpy as np


COLOURS = {
    "MUTATION OF FORMS": {
        "OFF WHITE": "#FAEFDD",
        "RED": "#CB0B22",
        "BLUE": "#1D119B",
    }
}


# For MUTATION OF FORMS
# See: https://www.metmuseum.org/art/collection/search/815337
number_points_per_side = 10
padding_per_side = 2
pad_points = 2


def create_angles_array(return_red=False, return_blue=False):
    """ TODO. """
    # NOTE: angles start pointing downwards i.e. 0 degs is south in PyPlot.
    # So red wedges are constrained to -135 to +45, blues to +45 to +225.

    # Original design angular coverage pattern is:
    #
    #     max blue ............. min blue
    #     min red  .............  max red
    #     ..    .                .     ..
    #     ..      .            .       ..
    #     ..        half blue          ..
    #     ..         half red          ..
    #     ..      .           .        ..
    #     ..    .               .      ..
    #     min blue ............. max blue
    #     max red  .............  min red

    # Define max and min angular coverages for the wedges:
    # * red wedges go from -135 <- -45 -> +45
    max_coverage_red = (-135, 45)
    min_coverage_red = -45
    # * blue wedges go from +45 <- +135 -> +225
    max_coverage_blue = (45, 225)
    min_coverage_blue = 135

    # Use linspace to get 1D arrays of angles evenly spaced across coverage
    red_theta1_min_to_max = np.linspace(
        max_coverage_red[0], min_coverage_red, num=number_points_per_side)
    red_theta2_min_to_max = np.linspace(
        max_coverage_red[1], min_coverage_red, num=number_points_per_side)
    blue_theta1_min_to_max = np.linspace(
        max_coverage_blue[0], min_coverage_blue, num=number_points_per_side)
    blue_theta2_min_to_max = np.linspace(
        max_coverage_blue[1], min_coverage_blue, num=number_points_per_side)

    # Zip up theta{1, 2} into an iterator to provide list of angle tuples later
    red_linspace_thetas = zip(red_theta1_min_to_max, red_theta2_min_to_max)
    blue_linspace_thetas = zip(blue_theta1_min_to_max, blue_theta2_min_to_max)

    if return_red:
        return list(red_linspace_thetas)
    elif return_blue:
        return list(blue_linspace_thetas)


def plot_wedges(position, red_wedge_thetas, blue_wedge_thetas):
    """ TODO. """
    red_wedge = plot_wedge(
        position, *red_wedge_thetas, COLOURS["MUTATION OF FORMS"]["RED"])
    blue_wedge = plot_wedge(
        position, *blue_wedge_thetas, COLOURS["MUTATION OF FORMS"]["BLUE"])
    return red_wedge, blue_wedge


def plot_wedge(centre, theta1, theta2, colour):
    """ TODO. """
    # 0.5 radius means the circles containing the wedges just touch their
    # neighbours. Use 0.475 radius to provide a small gap as in the design.
    return mpatches.Wedge(
        centre, 0.475, theta1, theta2, color=colour
    )


def plot_mutation_of_forms(axes):
    """ TODO. """

    grid_indices = range(number_points_per_side)
    red_spaced_thetas = create_angles_array(return_red=True)
    blue_spaced_thetas = create_angles_array(return_blue=True)
    for i, j in itertools.product(grid_indices, grid_indices):
        # Defaults for now while get the angles defined and in right places:
        red_thetas = (-90, 0)
        blue_thetas = (90, 180)

        # Process just outer-most positioned wedges to check angle processing.
        # TODO: consolidate this logic with the inner angle processing once
        # that is in.
        maximum_position = number_points_per_side - 1
        if i == 0:
            red_thetas = red_spaced_thetas[j]
            blue_thetas = blue_spaced_thetas[::-1][j]
        elif j == 0:
            red_thetas = red_spaced_thetas[i]
            blue_thetas = blue_spaced_thetas[::-1][i]
        elif i == maximum_position:
            red_thetas = red_spaced_thetas[::-1][j]
            blue_thetas = blue_spaced_thetas[j]
        elif j == maximum_position:
            red_thetas = red_spaced_thetas[::-1][i]
            blue_thetas = blue_spaced_thetas[i]

        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        red_wedge, blue_wedge = plot_wedges(
            position_xy, red_thetas, blue_thetas)
        axes.add_patch(red_wedge)
        axes.add_patch(blue_wedge)


# Format canvas to centre on image and remove all axes and related markings
fig, ax = plt.subplots(figsize=(6, 6))
plot_mutation_of_forms(ax)
fig.set_canvas(plt.gcf().canvas)
background_colour = COLOURS["MUTATION OF FORMS"]["OFF WHITE"]  # needed below
fig.patch.set_facecolor(background_colour)
limits = (
    number_points_per_side - padding_per_side,
    number_points_per_side + padding_per_side
)
ax.set_xlim(*limits)
ax.set_ylim(*limits)
plt.axis('equal')
plt.axis('off')
plt.xticks([])
plt.yticks([])
plt.tight_layout()

# Plot, save and show. Done!
plt.savefig(
    'img/mutation_of_forms.png',
    format='png',
    bbox_inches='tight',
    facecolor=background_colour,
)
plt.show()
