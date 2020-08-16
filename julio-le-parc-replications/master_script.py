import itertools

import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


COLOURS = {
    "MUTATION OF FORMS": {
        "OFF WHITE": "#F8F0DB",
        "RED": "#C8082D",
        "BLUE": "#1D119B",
    }
}


# For MUTATION OF FORMS
# See: https://www.metmuseum.org/art/collection/search/815337
number_points_per_side = 10
padding_per_side = 2
pad_points = 2

fig, ax = plt.subplots(figsize=(12, 12))


def plot_wedges(position):
    """ TODO. """
    red_wedge = plot_wedge(
        position, 270, 360, COLOURS["MUTATION OF FORMS"]["RED"])
    blue_wedge = plot_wedge(
        position, 90, 180, COLOURS["MUTATION OF FORMS"]["BLUE"])
    return red_wedge, blue_wedge


def plot_wedge(centre, theta1, theta2, colour):
    """ TODO. """
    # 0.5 radius means the circles containing the wedges just touch their
    # neighbours. Use 0.475 radius to provide a small gap as in the design.
    return mpatches.Wedge(
        centre, 0.475, theta1, theta2, color=colour
    )


grid_indices = range(number_points_per_side)
for i, j in itertools.product(grid_indices, grid_indices):
    position_xy = (pad_points + i, pad_points + j)
    red_wedge, blue_wedge = plot_wedges(position_xy)
    ax.add_patch(red_wedge)
    ax.add_patch(blue_wedge)


# Format canvas to centre on image and remove all axes and related markings
fig.set_canvas(plt.gcf().canvas)
fig.patch.set_facecolor(COLOURS["MUTATION OF FORMS"]["OFF WHITE"])
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

plt.show()
