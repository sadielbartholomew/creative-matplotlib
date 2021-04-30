import matplotlib.pyplot as plt
import numpy as np


# ---------- Tree parameters ------------
# Overall profile dimensions parameters:
height = 100.0
width = 100.0

# Angles:
initial_angle = 0.5 * np.pi
angle_between_segments = 0.05 * np.pi

# Trunk and branch length:
initial_length = 400.0  # length of trunk
length_scaling = 0.6

# Trunk and branch thickness:
initial_thickness = 0.1
# ---------------------------------------


def canopy_fractal_tree(x, y, length, theta):
    """Recursive formation of a canopy fractal tree-like profile."""
    if length >= 1.0:
        x_new = x + length * np.cos(theta)
        y_new = y + length * np.sin(theta)
        thickness = (
            initial_thickness * ((x_new - x) ** 2 + (y_new - y) ** 2) ** 0.5
        )
        plt.plot(
            (x, x_new),
            (y, y_new),
            color="black",
            linewidth=thickness,
            solid_capstyle="round",
        )
        new_length = length * length_scaling
        canopy_fractal_tree(
            x_new, y_new, new_length, theta + angle_between_segments
        )
        canopy_fractal_tree(
            x_new, y_new, new_length, theta - angle_between_segments
        )


def plot_single_tree_profile(index, param_label_name, param_label_value):
    """Plots a single tree profile which is shown and also saved."""
    plt.axes().set_aspect(1)
    plt.axis("off")
    canopy_fractal_tree(width, height, initial_length, initial_angle)
    plt.title(
        "Tree {}: parameter {} is '{}'".format(
            index, param_label_name, param_label_value
        )
    )
    plt.savefig("example-profiles/basic-canopy-fractal-{}.png".format(index))
    plt.show()


# Plot some representative examples:
for value in range(5):
    angle_between_segments
    plot_single_tree_profile(
        str(value + 1), "angle_between_segments", angle_between_segments
    )
    angle_between_segments *= 1.5
