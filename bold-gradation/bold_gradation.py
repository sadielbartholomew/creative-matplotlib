"""Bold Gradation: bold designs produced by subtle colour variation.

Created by Sadie L. Bartholomew, May 2022.

"""

from os.path import join

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
final_designs_done = {
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


def plot_and_save_all_designs():
    """Configures, plots and saves each design on a clean canvas."""
    for design_name, design in final_designs_done.items():
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
            join("designs", f"{design_name}.png"),
            bbox_inches="tight",
            dpi=1000,
        )

    plt.show()


plot_and_save_all_designs()
