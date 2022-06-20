"""Bold Gradation: bold designs produced by subtle colour variation.

Created by Sadie L. Bartholomew, May 2022.

"""

from os.path import join
from os import makedirs

import numpy as np
import matplotlib.pyplot as plt


# Global project configuration values for a general setup
samples = 5000
x = np.arange(samples) / samples - 0.5
y = np.arange(samples) / samples - 0.5
X, Y = np.meshgrid(x, y)


"""
Design name key with value being a list of all design parameters, in order:
    x_lims: 2-tuple of x-axis limits to set to crop the plot as desired;
    y_lims: 2-tuple of y-axis limits to set to crop the plot as desired;
    R: function to evaluate in terms of the X, Y meshgrid array;
    a: one-parameter function of above R to define the 2D data to display;
    colourmap: the built-in matplotlib colormap to use to supply colouring.

"""
final_designs_top_level = {
    "Union": [
        (1400, 3600),
        (1400, 3600),
        (1.6 * np.cos(X - Y)) + (1.5 * np.sin(Y ** 2)),
        lambda R: np.cos(np.pi * ((R ** 4))),
        "twilight_shifted",
    ],
    "Forth": [
        (350, 4850),
        (0, 4500),
        np.power(
            (X ** 5 - X ** 2) ** 2 + (Y ** 6 - Y ** 4 - Y ** 3) ** 2, 1 / 10
        ),
        lambda R: np.cos(np.pi * ((5 * R ** 3 - 20 * R ** 2))),
        "bone",
    ],
    "Vicinity": [
        (100, 1000),
        (3800, 4700),
        np.cos((Y ** 3 + np.pi - X ** 2) / (X ** 3 - Y ** 2))
        / (np.sinh(X - Y ** 2) + 1),
        lambda R: np.cos(R) - 1,
        "cubehelix_r",
    ],
}

final_designs_tubular_forms = {
    "Sharp Left": [
        (3300, 4200),
        (3800, 4700),
        np.power(
            (500 * X ** 7 - 10 * X ** 2) ** 4
            + (1000 * Y ** 7 - 3 * Y ** 4 - 5 * Y ** 2) ** 2,
            1 / 5,
        ),
        lambda R: np.cos(np.pi * ((5 * R ** 3 - 3 * R ** 2 + 20 * R))),
        "Reds",
    ],
    "Change of Motion": [
        (500, 2500),
        (1500, 3500),
        np.power(
            (500 * X ** 6 - 10 * X ** 2) ** 4
            + (1000 * Y ** 7 - 3 * Y ** 4 - 5 * Y ** 2) ** 2,
            1 / 5,
        ),
        lambda R: np.cos(np.pi * ((5 * R ** 3 - 3 * R ** 2 + 20 * R))),
        "Purples",
    ],
    "Object in the Foreground": [
        (280, 920),
        (560, 1200),
        np.power(
            (-100 * X ** 6 + 3 * X ** 2) ** 4
            + (200 * Y ** 7 - 15 * Y ** 4 - 10 * Y ** 3) ** 2,
            1 / 7,
        ),
        lambda R: np.cos(np.pi * ((5 * R ** 3 + 5 * R ** 2 + 20 * R))),
        "Blues",
    ],
    "Direct Approach": [
        (2200, 2800),
        (3500, 4100),
        np.power(
            (3000 * X ** 6 - 13 * X ** 2) ** 2
            + (800 * Y ** 5 - 133 * Y ** 4 - 5 * Y ** 2) ** 4,
            1 / 5,
        ),
        lambda R: np.sin(np.pi * ((R ** 3 - 3 * R ** 2 + 30 * R))),
        "Greens",
    ],
    "Sun to Plain": [
        (100, 1000),
        (1240, 2140),
        np.power(
            (4000 * Y ** 6 + 20 * Y ** 2) ** 2
            + (200 * X ** 6 - 77 * X ** 4 - 5 * X) ** 4,
            1 / 5,
        ),
        lambda R: np.sin(np.pi * ((R ** 7 - 3 * R ** 4 - 10 * R))),
        "Oranges",
    ],
}


def plot_design(design_name, design, save_path):
    """Configures, plots and saves each design on a clean canvas."""
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create design
    xlims, ylims, R, a, colourmap = design
    a_R = a(R)
    # Note: the use of image antialiasing was important for finding nice
    # designs from exploration of mathematical functions which could
    # produce areas of high complexity/detail, but it probably has little
    # if any effect on the outcomes from the final designs, as they focus
    # in on areas which vary only very gradually by manual selection.
    ax.imshow(a_R, interpolation="antialiased", cmap=colourmap)
    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)

    # Customise plot to hide all text then save to a dedicated directory
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_axis_off()

    fig.savefig(
        save_path,
        bbox_inches="tight",
        dpi=1000,
    )


def plot_and_save_all_designs():
    """Plots and saves all chosen designs."""
    parent_dir_name = "designs"

    # Top-level designs
    for design_name, design in final_designs_top_level.items():
        plot_design(
            design_name, design, join(parent_dir_name, f"{design_name}.png")
        )

    # Designs for a sub-project called 'Tubular Forms'
    for design_name, design in final_designs_tubular_forms.items():
        sub_dir_name = "tubular_forms"
        makedirs(join(parent_dir_name, sub_dir_name), exist_ok=True)
        save_dir = join(parent_dir_name, sub_dir_name, f"{design_name}.png")
        plot_design(design_name, design, save_dir)

    # Show all designs once generated and saved
    plt.show()


plot_and_save_all_designs()
