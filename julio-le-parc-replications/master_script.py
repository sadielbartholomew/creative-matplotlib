import itertools

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import numpy as np


"""
References (all from The Metropolitan Museum of Art)

* Mutation of Forms (1959):
    https://www.metmuseum.org/art/collection/search/815337
* Rotations (1959):
    https://www.metmuseum.org/art/collection/search/815346
* Rotation of Fractioned Circles (1959):
    https://www.metmuseum.org/art/collection/search/815341
* Rotation in Red and Black (1959):
    https://www.metmuseum.org/art/collection/search/815338

See also the Le Parc's website:
    http://www.julioleparc.org/
"""

COLOURS = {
    "MUTATION OF FORMS": {
        "OFF WHITE": "#FAEFDD",
        "RED": "#CB0B22",
        "BLUE": "#1D119B",
    },
    "ROTATIONS": {
        "OFF WHITE": "#F9F2E9",
        "OFF BLACK": "#161815",
    },
    "ROTATION OF FRACTIONED CIRCLES": {
        "OFF WHITE": "#F5EFE3",
        "LIGHT GREY": "#D3D2D0",
        "DARK GREY": "#63676B",
    },
    "ROTATION IN RED AND BLACK": {
        "OFF WHITE": "#F2ECE0",
        "OFF BLACK": "#100F0D",
        "RED": "A41425",  # 983134 is a nice red,
    },
}
NUMBER_GRIDPOINTS_PER_SIDE = {
    "MUTATION OF FORMS": 10,
    "ROTATIONS": 13,
    "ROTATION OF FRACTIONED CIRCLES": 9,
    "ROTATION IN RED AND BLACK": 10,
}

number_points_per_side = 10
grid_indices = range(number_points_per_side)


def create_linspaced_angles(max_coverage, min_coverage):
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
    # * blue wedges go from +45 <- +135 -> +225

    # Use linspace to get 1D arrays of angles evenly spaced across coverage:
    theta1_min_to_max = np.linspace(
        max_coverage[0], min_coverage[0], num=number_points_per_side)
    theta2_min_to_max = np.linspace(
        max_coverage[1], min_coverage[1], num=number_points_per_side)

    return np.column_stack((theta1_min_to_max, theta2_min_to_max))


def create_angles_array(is_red=True):
    """ TODO. """
    angles_array = np.zeros(
        (number_points_per_side, number_points_per_side),
        dtype=(float, 2)
    )

    if is_red:
        index = 1
        spaced_thetas = create_linspaced_angles(
            max_coverage=(-135, 45), min_coverage=(-45, -45))
    else:
        index = -1
        spaced_thetas = create_linspaced_angles(
            max_coverage=(45, 225), min_coverage=(135, 135))

    # 1. Make first and last column correct:
    for j in grid_indices:
        angles_array[0][j] = spaced_thetas[::index][j]
        angles_array[-1][j] = spaced_thetas[::index][-j-1]
    # 2. Create rows linearly-spaced based on first and last columns:
    for i in grid_indices:
        row_angles = create_linspaced_angles(
            max_coverage=angles_array[0][i],
            min_coverage=angles_array[-1][i],
        )
        angles_array[i] = row_angles

    return angles_array


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
    pad_points = 2
    for i, j in itertools.product(grid_indices, grid_indices):
        # Defaults for now while get the angles defined and in right places:
        red_thetas = create_angles_array(is_red=True)[i][j]
        blue_thetas = create_angles_array(is_red=False)[i][j]

        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        red_wedge, blue_wedge = plot_wedges(
            position_xy, red_thetas, blue_thetas)
        axes.add_patch(red_wedge)
        axes.add_patch(blue_wedge)


def format_canvas(design_name):
    """ TODO. """
    # Format canvas to centre on image and remove all axes and related markings
    fig, ax = plt.subplots(figsize=(6, 6))
    plot_mutation_of_forms(ax)
    fig.set_canvas(plt.gcf().canvas)
    background_colour = COLOURS[design_name]["OFF WHITE"]  # needed for savefig
    fig.patch.set_facecolor(background_colour)

    padding_per_side = 2
    limits = (
        NUMBER_GRIDPOINTS_PER_SIDE[design_name] - padding_per_side,
        NUMBER_GRIDPOINTS_PER_SIDE[design_name] + padding_per_side
    )

    ax.set_xlim(*limits)
    ax.set_ylim(*limits)
    plt.axis('equal')
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()

    return background_colour  # pass through for savefig


# 1. Plot Mutation of Forms:
background_col = format_canvas("MUTATION OF FORMS")
plt.savefig(
    'img/mutation_of_forms/replication_of_original.png',
    format='png',
    bbox_inches='tight',
    facecolor=background_col,
)
plt.show()

# 2. Plot Rotations:
# ...
# 3. Plot Rotation of Fractioned Circles:
# ...
# 4. Plot Rotation in Red and Black:
# ...
