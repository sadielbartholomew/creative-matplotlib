from itertools import cycle
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ---------- Design and output parameters ------------
# ... for container shape, outer to all the other shapes:
outer_size = 0.5
outer_centre = (0.5, 0.5)

# ... for the design of inner shapes:
size_ratio_of_next_inner_shape = 0.07
# For the alternative designs as shown in the README gallery, instead set 0.03
number_inner_shapes = 500

# ... for the (cycling) colours of the shapes:
background_colour = "black"
# For the alternative designs, instead set the above to "white"
# Choose a set of harmonious 'mod' like colours that are bold but not garish
stage_one_colours = [
    "midnightblue",
    "lavender",
    "crimson",
    "dodgerblue",
    "indianred",
]
# For the alternative designs in the README gallery, instead set the above to:
# ["black", "peru", "darkslategrey", "goldenrod", "teal", "wheat"]
stage_one_colour_selector = cycle(stage_one_colours)
stage_two_colours = [
    "darkslategrey",
    "khaki",
    "lightseagreen",
    "azure",
    "indigo",
    "powderblue",
]
stage_two_colour_selector = cycle(stage_two_colours)


# ... directories to save designs into:
first_level_dir = "img"  # second_level_dirs live separately under this dir
second_level_dirs = [
    "without-random-edge-alignment",
    "with-random-edge-alignment",
]
# For the alternative designs, add "-alt" to the end of both dirs above

# List all designs to create...
number_sides_to_plot_compound = [1, 4, 3, 5]  # 3 <-> 4 for overall symmetry
number_sides_to_plot_as_single = number_sides_to_plot_compound + [7, 12]

# ... with the (empirically determined) mapping to zoom in to achieve a
# close-up on the container shape without any of the background showing.
# Note that the higher the value, the less zoomed in, up to 0.5 which results
# in no zoom-in relative to the standard designs (with 'closeup=False')
zoom_in_factors = {
    1: 0.27,
    3: 0.18,  # note this is also shifted down by ~0.1 later to re-centralise
    4: 0.215,
    5: 0.24,
    7: 0.25,
    12: 0.27,
}

# -----------------------------------------


def make_shape(
        centre, size, sides=1, colour_selector=stage_one_colour_selector):
    """TODO."""
    # Could take the (number of) sides -> infinity for sides of a regular
    # polygon to approximate a circle, but better to use actual circular
    # matplotlib patch as a special case:
    if sides == 1:
        size *= 0.9  # make slightly smaller so relatively in size w/ polygons
        return mpatches.Circle(centre, size, facecolor=next(colour_selector))
    elif sides == 2:
        raise ValueError(
            "No two-sided regular polygon, choose another 'sides' value!"
        )
    else:  # regular polygon patch of specified number of sides
        if sides == 3:
            # Make size larger else triangle looks a bit small in relation and
            # also shift downwards to fit larger shape in the axes boundaries
            size *= 1.1
            centre_x, centre_y = centre
            centre = centre_x, centre_y - 0.1
        return mpatches.RegularPolygon(
            centre, sides, size, facecolor=next(colour_selector)
        )


def make_design_patches(sides=1):
    """TODO."""
    patch_layers = []

    # zorder managed naturally via plotting largest first, if did in inverse
    # order would need to use zorder to stop larger shapes covering smaller.
    new_size = outer_size
    for _ in range(number_inner_shapes):
        new_size *= 1 - size_ratio_of_next_inner_shape
        patch_layers.append(make_shape(outer_centre, new_size, sides))

    return patch_layers


def create_design(axes, sides=1):
    """TODO."""
    for p in make_design_patches(sides=sides):
        axes.add_artist(p)


def plot_and_save(use_number_of_sides=1, single=True, closeup=False):
    """TODO."""
    fig = plt.figure(figsize=(5, 5), facecolor=background_colour)

    if single:
        ax = fig.add_subplot(111, aspect="equal")
        create_design(ax, sides=use_number_of_sides)
    else:
        # Vary subplot_index prefix appropriate to len(use_number_of_sides)
        for i, set_sides in enumerate(use_number_of_sides):
            subplot_index = 2
            ax = fig.add_subplot(subplot_index, subplot_index, i + 1)
            ax.set_facecolor(background_colour)
            ax.set_axis_off()
            create_design(ax, sides=set_sides)

    plt.axis("off")

    if single:
        name_prefix = f"single_design_with_{use_number_of_sides}_sides"
    else:
        name_prefix = "compound_design"

    # Create dirs to store the output designs if they do not exist already
    os.makedirs(f"{first_level_dir}", exist_ok=True)
    for directory in second_level_dirs:
        os.makedirs(f"{first_level_dir}/{directory}", exist_ok=True)
        os.makedirs(
            f"{first_level_dir}/{directory}-closeups",
            exist_ok=True
        )

    # Now can plot, save and show the final single or compound design
    directory = f"{first_level_dir}/{second_level_dirs[0]}"
    if closeup and single:
        # Zoom in on single plots if requested
        zoom_in_factor = zoom_in_factors[use_number_of_sides]
        zoom_in_vals = (0.5 - zoom_in_factor, 0.5 + zoom_in_factor)  # min, max
        if use_number_of_sides == 3:
            shifted_down_zoom_in_vals = (
                0.405 - zoom_in_factor, 0.405 + zoom_in_factor)
            zoom_in_vals = zoom_in_vals + shifted_down_zoom_in_vals
        else:  # x and y axes min and max are the same
            zoom_in_vals += zoom_in_vals  
        ax.axis(zoom_in_vals)

        # For the alternative designs, add "_alt" to the end of the filename
        # before the extension to save to the dirs as in the savde repo state:
        plt.savefig(
            f"{directory}-closeups/{name_prefix}_closeup.png",
            format="png",
            dpi=1000,
            bbox_inches='tight',
        )
        plt.show()
    else:
        #  For the alternative designs, add "_alt" (see above comment)
        plt.savefig(
            f"{directory}/{name_prefix}.png",
            format="png",
            dpi=1000,
        )
        plt.show()


# Create and plot the designs from...
# ...without zooming in:
for number_sides in number_sides_to_plot_as_single:
    plot_and_save(use_number_of_sides=number_sides)
plot_and_save(single=False, use_number_of_sides=number_sides_to_plot_compound)
# ... zooming in to create a close-up where the shapes fill the entire canvas:
for number_sides in number_sides_to_plot_as_single:
    plot_and_save(use_number_of_sides=number_sides, closeup=True)
