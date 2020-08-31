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
        "RED": "#983134",
    },
}
NUMBER_GRIDPOINTS_PER_SIDE = {
    "MUTATION OF FORMS": 10,
    "ROTATIONS": 13,
    "ROTATION OF FRACTIONED CIRCLES": 9,
    "ROTATION IN RED AND BLACK": 10,
}


pad_points = 2
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


def create_mutation_angles_array(grid_indices, is_red=True):
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


def plot_mutations_wedges(
        position, wedge_1_thetas, wedge_2_thetas, colour_1, colour_2):
    """ TODO. """
    wedge_1 = plot_mutations_wedge(position, *wedge_1_thetas, colour_1)
    wedge_2 = plot_mutations_wedge(position, *wedge_2_thetas, colour_2)
    return wedge_1, wedge_2


def plot_mutations_wedge(centre, theta1, theta2, colour):
    """ TODO. """
    # 0.5 radius means the circles containing the wedges just touch their
    # neighbours. Use 0.475 radius to provide a small gap as in the design.
    return mpatches.Wedge(
        centre, 0.475, theta1, theta2, color=colour
    )


def plot_rotations_patch(centre, colour):
    """ TODO. """
    return mpatches.Circle(
        centre, 0.475, color=colour
    )


def plot_fractioned_circle_patch(centre, colour):
    """ TODO. """
    return mpatches.Circle(
        centre, 0.475, color=colour
    )


def plot_simple_cross(centre, base_theta, colour_1, colour_2):
    """ TODO. """
    # Define two lines perpendicular to each other as patches
    length = 0.7
    width = 0.05
    cen_1, cen_2 = centre[0], centre[1]

    # Adding and subtracting some width/length so central despite any width:
    line_1 = mpatches.Rectangle(
        (cen_1 - width, cen_2 + (length-width) / 2.0),
        length, width, base_theta, color=colour_1)
    line_2 = mpatches.Rectangle(
        (cen_1 + (length-width) / 2.0, cen_2),
        length, width, base_theta + 90, color=colour_2
    )
    return line_1, line_2


def plot_mutation_of_forms(axes):
    """ TODO. """
    design_name = "MUTATION OF FORMS"
    grid_points = range(NUMBER_GRIDPOINTS_PER_SIDE[design_name])
    for i, j in itertools.product(grid_points, grid_points):
        red_thetas = create_mutation_angles_array(
            is_red=True, grid_indices=grid_points)[i][j]
        blue_thetas = create_mutation_angles_array(
            is_red=False, grid_indices=grid_points)[i][j]

        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        red_wedge, blue_wedge = plot_mutations_wedges(
            position_xy, red_thetas, blue_thetas,
            colour_1=COLOURS[design_name]["RED"],
            colour_2=COLOURS[design_name]["BLUE"],
        )
        axes.add_patch(red_wedge)
        axes.add_patch(blue_wedge)


def plot_rotations(axes):
    """ TODO. """
    design_name = "ROTATIONS"
    grid_points = range(NUMBER_GRIDPOINTS_PER_SIDE[design_name])
    for i, j in itertools.product(grid_points, grid_points):
        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        axes.add_patch(plot_rotations_patch(
            position_xy,
            colour=COLOURS[design_name]["OFF BLACK"],
        ))


def plot_rotation_of_fractioned_circles(axes):
    """ TODO. """
    design_name = "ROTATION OF FRACTIONED CIRCLES"
    grid_points = range(NUMBER_GRIDPOINTS_PER_SIDE[design_name])
    for i, j in itertools.product(grid_points, grid_points):
        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        axes.add_patch(plot_fractioned_circle_patch(
            position_xy, colour=COLOURS[design_name]["LIGHT GREY"]))


def plot_rotation_in_red_and_black(axes):
    """ TODO. """
    design_name = "ROTATION IN RED AND BLACK"
    grid_points = range(
        NUMBER_GRIDPOINTS_PER_SIDE[design_name])
    for i, j in itertools.product(grid_points, grid_points):
        # Now create and plot the wedges onto the canvas:
        position_xy = (pad_points + i, pad_points + j)
        red_line, black_line = plot_simple_cross(
            position_xy, 0,
            COLOURS[design_name]["RED"],
            COLOURS[design_name]["OFF BLACK"],
        )
        axes.add_patch(red_line)
        axes.add_patch(black_line)


def format_canvas(design_name, patch_creation_func):
    """ TODO. """
    # Format canvas to centre on image and remove all axes and related markings
    fig, ax = plt.subplots(figsize=(6, 6))
    patch_creation_func(ax)
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


def plot_and_save_design(design_name, plot_func, save_dir):
    background_col = format_canvas(design_name, plot_func)
    plt.savefig(
        'img/{}/replication_of_original.png'.format(save_dir),
        format='png',
        bbox_inches='tight',
        facecolor=background_col,
    )


# Plot all four designs
# TODO: note that only 1 is complete, 3-4 are yet to be fully coded up
plot_and_save_design(
    "MUTATION OF FORMS", plot_mutation_of_forms, "mutation_of_forms")
plot_and_save_design("ROTATIONS", plot_rotations, "rotations")
plot_and_save_design(
    "ROTATION OF FRACTIONED CIRCLES", plot_rotation_of_fractioned_circles,
    "rotation_of_fractioned_circles"
)
plot_and_save_design(
    "ROTATION IN RED AND BLACK", plot_rotation_in_red_and_black,
    "rotation_in_red_and_black"
)

plt.show()
