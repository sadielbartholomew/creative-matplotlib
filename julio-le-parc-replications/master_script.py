import itertools

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms

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
        "OFF WHITE": "#F4EDE5",
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


IMAGE_PAD_POINTS = 2


def create_mutations_linspaced_angles(
        max_coverage, min_coverage, number_points_per_side):
    """ TODO.

    NOTE: angles start pointing downwards i.e. 0 degs is south in PyPlot.
    So red wedges are constrained to -135 to +45, blues to +45 to +225.

    Original design angular coverage pattern is:

         max blue ............. min blue
         min red  .............  max red
         ..            ..             ..
         ..            ..             ..
         ...........half blue...........
         ...........half red............
         ..            ..             ..
         ..            ..             ..
         min blue ............. max blue
         max red  .............  min red

    Define max and min angular coverages for the wedges:
    * red wedges go from -135 <- -45 -> +45
    * blue wedges go from +45 <- +135 -> +225
    """

    # Use linspace to get 1D arrays of angles evenly spaced across coverage:
    theta1_min_to_max = np.linspace(
        max_coverage[0], min_coverage[0], num=number_points_per_side)
    theta2_min_to_max = np.linspace(
        max_coverage[1], min_coverage[1], num=number_points_per_side)

    return np.column_stack((theta1_min_to_max, theta2_min_to_max))


def create_mutation_angles_array(
        grid_indices, is_red=True, number_points_per_side=5):
    """ TODO. """
    red_max = (-135, 45)
    red_min = (-45, -45)
    blue_max = (45, 225)
    blue_min = (135, 135)

    angles_array = np.zeros(
        (number_points_per_side, number_points_per_side),
        dtype=(float, 2)
    )

    if is_red:
        index = 1  # don't change the spaced_thetas array later (c.f. -1)
        spaced_thetas = create_mutations_linspaced_angles(
            max_coverage=red_max, min_coverage=red_min,
            number_points_per_side=number_points_per_side,
        )
    else:
        index = -1  # to reverse the spaced_thetas array later, via [::-1]
        spaced_thetas = create_mutations_linspaced_angles(
            max_coverage=blue_max, min_coverage=blue_min,
            number_points_per_side=number_points_per_side,
        )

    # 1. Make first and last column correct:
    for j in grid_indices:
        angles_array[0][j] = spaced_thetas[::index][j]
        angles_array[-1][j] = spaced_thetas[::index][-j-1]
    # 2. Create rows linearly-spaced based on first and last columns:
    for i in grid_indices:
        row_angles = create_mutations_linspaced_angles(
            max_coverage=angles_array[0][i],
            min_coverage=angles_array[-1][i],
            number_points_per_side=number_points_per_side,
        )
        angles_array[i] = row_angles

    return angles_array


def create_rotations_angles_array(
        grid_indices, number_points_per_side=5):
    """ TODO. """
    angles_array = np.zeros(
        (number_points_per_side, number_points_per_side),
        dtype=float
    )

    spaced_thetas = np.linspace(0, 180, number_points_per_side)
    # 1. Make first and last column correct:
    for j in grid_indices:
        angles_array[0][j] = spaced_thetas[j]
        angles_array[-1][j] = spaced_thetas[-j-1]
    # 2. Create rows linearly-spaced based on first and last columns:
    for i in grid_indices:
        # Minus sign is to achieve clockwise angle changes as per the design.
        # Without it the angles would move from the first to the last angles
        # in an anti-clockwise direction:
        row_angles = np.linspace(
            -1 * angles_array[0][i],  # see above regarding -1 factor
            angles_array[-1][i],
            number_points_per_side,
        )
        angles_array[i] = row_angles

    return angles_array


def create_fractioned_angles_array(
        grid_indices, number_points_per_side):
    """ TODO. """

    angles_array = np.zeros(
        (number_points_per_side, number_points_per_side),
        dtype=float
    )

    first_col_thetas = np.linspace(-70, 70, number_points_per_side)
    last_col_thetas = np.linspace(70, 3 * 360 + 290, number_points_per_side)

    # 1. Make first and last column correct:
    for j in grid_indices:
        angles_array[0][j] = first_col_thetas[j]
        angles_array[-1][j] = last_col_thetas[j]
    # 2. Create rows linearly-spaced based on first and last columns:
    for i in grid_indices:
        row_angles = np.linspace(
            angles_array[0][i],
            angles_array[-1][i],
            number_points_per_side,
        )
        angles_array[i] = row_angles

    return -1 * np.flip(angles_array, axis=1)


def plot_mutations_wedges(
        position, wedge_1_thetas, wedge_2_thetas, colour_1, colour_2):
    """ TODO. """
    wedge_1 = plot_mutations_wedge(position, *wedge_1_thetas, colour_1)
    wedge_2 = plot_mutations_wedge(position, *wedge_2_thetas, colour_2)
    return wedge_1, wedge_2


def plot_mutations_wedge(centre, theta1, theta2, colour):
    """ TODO. """
    # 0.5 radius means the circles containing the wedges just touch their
    # neighbours. Use 0.475 radius to provide a small gap as per the design.
    return mpatches.Wedge(
        centre, 0.475, theta1, theta2, color=colour
    )


def plot_rotations_patch(
        centre, rect_angle, foreground_colour, background_colour, ax):
    """ TODO. """
    # These parameters are adapted to match the original design:
    radius = 0.45
    offset_amount = 0.3
    padding = 0.03

    # Note: get a very thin but still visible edge line on circle even if set
    # linewidth to zero, so to workaround make edgecolour background colour.
    patch = mpatches.Circle(
        centre, radius, facecolor=foreground_colour,
        edgecolor=background_colour,
    )
    # The clipping rectangle, rotated appropriately (no need to rotate circle!)
    clip_patch = mpatches.Rectangle(
        (centre[0] + offset_amount, centre[1] - radius),
        radius - offset_amount + padding,
        2 * radius, color=background_colour,
        transform=mtransforms.Affine2D().rotate_deg_around(
            *centre, rect_angle) + ax.transData
    )
    return (patch, clip_patch)


def plot_fractioned_circle_patch(
        centre, rect_angle, dark_colour, light_colour, background_colour, ax):
    """ TODO. """
    # These parameters are adapted to match the original design:
    radius = 0.45
    offset_amount = 0.02
    light_offset = 0.5
    padding = 0.03
    line_size = 0.12

    # Note: get a very thin but still visible edge line on circle even if set
    # linewidth to zero, so to workaround make edgecolour background colour.
    light_patch = mpatches.Circle(
        centre, radius, facecolor=light_colour,
        edgecolor=background_colour,
    )
    start_at = (centre[0] + offset_amount, centre[1] - radius)
    clip_alpha = 3
    # The clipping rectangle, rotated appropriately (no need to rotate circle!)
    clip_patch = mpatches.Rectangle(
        start_at,
        line_size,
        2 * radius, color=background_colour,
        transform=mtransforms.Affine2D().rotate_deg_around(
            *centre, rect_angle) + ax.transData,
        alpha=clip_alpha
    )
    dark_patch = mpatches.Rectangle(
        start_at,
        radius,
        2 * radius, color=dark_colour,
        transform=mtransforms.Affine2D().rotate_deg_around(
            *centre, rect_angle) + ax.transData,
        alpha=clip_alpha - 1,
    )
    return (dark_patch, light_patch, clip_patch)


def create_cross_line(ax, centre, length, width, colour, angle):
    """ TODO. """
    lines = []
    for theta in (angle, angle + 180):  # two parallel half-lines from centre
        lines.append(
            mpatches.Rectangle(
                (centre[0] - width, centre[1] - (width / 2.0)),  # normalised
                length, width, color=colour,
                transform=mtransforms.Affine2D().rotate_deg_around(
                    *centre, theta) + ax.transData,
            )
        )
    return lines


def plot_simple_cross(centre, base_theta, colour_1, colour_2, ax):
    """ TODO. """
    half_length = 0.5
    width = 0.05

    # Define two lines perpendicular to each other as patches
    cross_lines = (
        create_cross_line(
            ax, centre, half_length, width, colour_1, base_theta) +
        create_cross_line(
            ax, centre, half_length, width, colour_2,
            base_theta + 90
        )
    )

    return cross_lines


def plot_mutation_of_forms(axes):
    """ TODO. """
    design_name = "MUTATION OF FORMS"
    points = NUMBER_GRIDPOINTS_PER_SIDE[design_name]
    grid_points = range(points)

    # Calculate angles:
    red_angles_array = create_mutation_angles_array(
        is_red=True, grid_indices=grid_points,
        number_points_per_side=points
    )
    blue_angles_array = create_mutation_angles_array(
        is_red=False, grid_indices=grid_points,
        number_points_per_side=points
    )
    for i, j in itertools.product(grid_points, grid_points):
        # Get angles:
        red_thetas = red_angles_array[i][j]
        blue_thetas = blue_angles_array[i][j]

        # Now create and plot the wedges onto the canvas:
        position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
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
    points = NUMBER_GRIDPOINTS_PER_SIDE[design_name]
    grid_points = range(points)

    angles_array = create_rotations_angles_array(
        grid_points,
        number_points_per_side=points
    )
    for i, j in itertools.product(grid_points, grid_points):
        position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
        circle, clipping_rectangle = plot_rotations_patch(
            position_xy,
            angles_array[i][j],
            COLOURS[design_name]["OFF BLACK"],
            COLOURS[design_name]["OFF WHITE"],
            axes,
        )
        axes.add_patch(circle)
        clipping_rectangle.set_clip_path(circle)
        axes.add_patch(clipping_rectangle)


def plot_rotation_of_fractioned_circles(axes):
    """ TODO. """
    design_name = "ROTATION OF FRACTIONED CIRCLES"
    points = NUMBER_GRIDPOINTS_PER_SIDE[design_name]
    grid_points = range(points)

    angles_array = create_fractioned_angles_array(
        grid_points,
        number_points_per_side=points
    )
    for i, j in itertools.product(grid_points, grid_points):
        position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
        dark_cir, light_cir, off_white_line = plot_fractioned_circle_patch(
            position_xy,
            angles_array[i][j],
            COLOURS[design_name]["DARK GREY"],
            COLOURS[design_name]["LIGHT GREY"],
            COLOURS[design_name]["OFF WHITE"],
            axes,
        )
        axes.add_patch(light_cir)
        dark_cir.set_clip_path(light_cir)
        axes.add_patch(dark_cir)
        off_white_line.set_clip_path(light_cir)
        axes.add_patch(off_white_line)


def plot_rotation_in_red_and_black(axes):
    """ TODO. """
    design_name = "ROTATION IN RED AND BLACK"
    points = NUMBER_GRIDPOINTS_PER_SIDE[design_name]
    grid_points = range(points)

    # TODO: using RoFC angles array as a placeholder. Find actual!
    angles_array = create_fractioned_angles_array(
        grid_points,
        number_points_per_side=points
    )
    for i, j in itertools.product(grid_points, grid_points):
        # Now create and plot the wedges onto the canvas:
        position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
        line_patches = plot_simple_cross(
            position_xy, angles_array[i][j],
            COLOURS[design_name]["RED"],
            COLOURS[design_name]["OFF BLACK"],
            axes
        )
        for line in line_patches:
            axes.add_patch(line)


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

    # For creating unique names to save generated variations whilst trying
    # to get the angles the same as the original(!):
    # # import uuid
    plt.savefig(
        'img/{}/replication_of_original.png'.format(save_dir),
        # # 'img/rotation_in_red_and_black/misc_variations/'
        # # '{}.png'.format(uuid.uuid4()),
        format='png',
        bbox_inches='tight',
        facecolor=background_col,
    )


# Plot all four designs
"""
plot_and_save_design(
    "MUTATION OF FORMS", plot_mutation_of_forms, "mutation_of_forms")
plot_and_save_design("ROTATIONS", plot_rotations, "rotations")
plot_and_save_design(
    "ROTATION OF FRACTIONED CIRCLES", plot_rotation_of_fractioned_circles,
    "rotation_of_fractioned_circles"
)
"""
plot_and_save_design(
    "ROTATION IN RED AND BLACK", plot_rotation_in_red_and_black,
    "rotation_in_red_and_black"
)

plt.show()
