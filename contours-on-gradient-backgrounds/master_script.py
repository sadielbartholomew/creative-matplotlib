"""Designs for contours on gradient backgrounds, created by Sadie
Bartholomew."""

import numpy as np
import matplotlib.pyplot as plt


""" Define data for all contour-on-gradient designs in a single dictionary.

Dictionary keys are the design names, comprising:

    1. 1_vortices
    2. 2_seams
    3. 3_star
    4. 4_sweep
    5. 5_circuitry
    6. 6_lattice
    7. 7_warped
    8. 8_jagged
    9. 9_ripples
    10. 10_whirls
    11. 11_panels
    12. 12_cellular
    13. 13_interlocking

where corresponding values are tuples of all data defining each, with items:

    contour_function:
        two-variable function (in u and v) defining the contours
    background_function:
        two-variable function (in u and v) defining the background gradient

    grid_resolution:
        integer defining the resolution for both axes for the meshgrid which
        the contours inhabit

    grid_limits:
        4-tuple defining the x and y limits of the contour-residing meshgrid
    view_limits:
        4-tuple defining the x and y axes limits of the overall design view
    background_limits:
        4-tuple defining the x and y limits for the area over which the
        background gradient is plotted

    linewidth_parameters:
        3-tuple defining arguments to numpy.arange specifying the line widths

    contour_colourmap:
        matplotlib colormap defining the colouring of the contours
    background_colourmap:
        matplotlib colormap defining the colouring of the background gradient
"""
DESIGNS = {
    "1_vortices": (
        lambda u, v: np.sinh(v / 10) ** 2
        - (np.sin(u * v) * np.cos(3 * v)) ** 2
        + 0.1,
        lambda u, v: -3 * v ** 4 + v ** 2 - v,
        1000,
        (-9, 9, -9, 9),
        (-2.5, 2.5, 4, 9),
        (-2.5, 2.5, 4, 9),
        (1.5, 4, 0.5),
        "afmhot",
        "YlOrRd",
    ),
    "2_seams": (
        lambda u, v: 0.002 * np.sin((u + v) ** -1) * np.cosh(u * v) ** -2
        + np.exp(-u * v ** 2),
        lambda u, v: (u + v) ** 5,
        30,
        (-0.06, 0.06, -0.06, 0.06),
        (-0.06, 0.06, -0.06, 0.06),
        (-0.06, 0.06, -0.06, 0.06),
        (1, 3, 0.5),
        "seismic",
        "BuPu",
    ),
    "3_star": (
        lambda u, v: 0.001
        * np.tanh(np.cos(-10 * u * v ** 2) ** -3 * np.exp(u ** -2 * v ** 5)),
        lambda u, v: (u + v) ** 4,
        300,
        (-5, 5, -5, 6),
        (-1.2, 1.2, 3.0, 5.4),
        (-5, 5, -5, 6),
        (0.5, 2.0, 0.5),
        "gnuplot",
        "gnuplot2_r",
    ),
    "4_sweep": (
        lambda u, v: np.arcsin(
            (np.exp(np.sin(0.9999 * u + v ** 2)) / (v / u + u - 0.001))
        )
        - 0.001 * v * np.sinh(0.01 * u * v) / u
        + v * np.sin(u * v)
        - u,
        lambda u, v: -0.5 * v ** 3 / u + u ** 0.3,
        700,
        (-12, 12, -12, 12),
        (4, 12, 4, 12),
        (-12, 12, -12, 12),
        (3, 4, 1),
        "terrain",
        "CMRmap",
    ),
    "5_circuitry": (
        lambda u, v: np.arctan((v * np.sin(30 * u / v)) ** -3),
        lambda u, v: 200000 * u / v ** 0.8 + 0.33,
        800,
        (-0.5, 0.5, -0.5, 0.5),
        (0.37, 0.39, -0.003, 0.017),
        (-0.5, 0.5, -0.5, 0.5),
        (2, 3, 0.5),
        "ocean_r",
        "gist_earth_r",
    ),
    "6_lattice": (
        lambda u, v: (v ** 2 / np.sin(u ** 2) - u ** 2 / np.cos(v ** 2))
        * np.tanh(u * v),
        lambda u, v: -(u ** 1.15) * v ** 1.15
        - u ** 1.1 / v ** 1.1
        + v ** 1.1 / u ** 1.1,
        1000,
        (-21.5, 21.5, -21.5, 21.5),
        (15, 21.5, 15, 21.5),
        (-21.5, 21.5, -21.5, 21.5),
        (1, 3, 0.5),
        "PRGn",
        "gnuplot2_r",
    ),
    "7_warped": (
        lambda u, v: v ** 2 * np.tan(u) - u ** 2 * np.sin(v),
        lambda u, v: np.sin(v) * np.abs(v) ** 0.5,
        1000,
        (-150, 150, -150, 150),
        (-80, 80, -80, 80),
        (-150, 150, -150, 150),
        (2, 3, 0.5),
        "terrain",
        "gist_heat",
    ),
    "8_jagged": (
        lambda u, v: np.sin(np.exp((u - v) / (u + u / v))),
        lambda u, v: u - v ** 2,
        600,
        (-20, 20, -20, 20),
        (0.3, 1.3, -2.3, -1.3),
        (-20, 20, -20, 20),
        (2, 5, 1),
        "rainbow",
        "gnuplot_r",
    ),
    "9_ripples": (
        lambda u, v: np.exp(-0.1 * v ** -2)
        * (
            (np.cos(0.2 * v ** 5 - u ** 4 + u * v ** 3)) ** 7
            + np.cos(-0.01 * u * v)
            - np.sin(-0.2 * u * v)
        ),
        lambda u, v: (u + v) ** 1.5,
        90,
        (2, 22, 2, 22),
        (2, 22, 2, 22),
        (2, 22, 2, 22),
        (2, 3, 1),
        "terrain",
        "YlGnBu_r",
    ),
    "10_whirls": (
        lambda u, v: np.sin((u - v) * np.exp(v - u) * np.cosh(v))
        + np.cos((u - v) * np.exp(v - u) * np.sinh(v)),
        lambda u, v: -np.abs(u) ** 0.3,
        1000,
        (-5, 5, -5, 5),
        (-3.8, -2.6, -1.2, 0.0),
        (-5, 5, -5, 5),
        (2, 3, 1),
        "gist_earth",
        "cubehelix",
    ),
    "11_panels": (
        lambda u, v: np.tanh(3 * u) * np.tanh(3 * v) * np.sin(u + 2 * v),
        lambda u, v: 2 * v + u,
        800,
        (-8.1, 8.1, -8.1, 8.1),
        (-8, 8, -8, 8),
        (-8.1, 8.1, -8.1, 8.1),
        (2, 6, 2),
        "RdBu_r",
        "RdBu",
    ),
    "12_cellular": (
        lambda u, v: np.arctanh((v * u ** -2) / (u * v))
        * np.cos(u ** 3 / (u ** -0.5 * v ** 2))
        * u ** -v,
        lambda u, v: (u - v) ** 4,
        1500,
        (1, 1.05, 0, 1),
        (1.01, 1.025, 0.015, 0.03),
        (1, 1.05, 0, 1),
        (2, 6, 2),
        "summer",
        "YlGn_r",
    ),
    "13_interlocking": (
        lambda u, v: np.cosh(np.sin(-100 * u + 10 * v))
        / (np.log(np.abs(v ** -1)) + 1),
        lambda u, v: u - 3 * v,
        1000,
        (1, 2.02, 1, 2.02),
        (1.02, 1.98, 1.02, 1.98),
        (1, 2.02, 1, 2.02),
        (3, 5, 1),
        "gist_stern",
        "BuPu_r",
    ),
}


# Define a chosen design to plot and unpack its data to use.
design_choice = "13_interlocking"
(
    contour_function,
    background_function,
    grid_resolution,
    axes_limits,
    view_limits,
    background_limits,
    linewidth_parameters,
    contour_colourmap,
    background_colourmap,
) = DESIGNS[design_choice]

# Set the figure dimensions and hide the axes ticks and labels.
x, y = np.meshgrid(
    np.linspace(*axes_limits[:2], num=grid_resolution),
    np.linspace(*axes_limits[-2:], num=grid_resolution),
)

plt.xticks([])
plt.yticks([])
plt.axis(view_limits)

# Plot the background.
plt.imshow(
    background_function(x, y),
    extent=background_limits,
    interpolation="bilinear",
    origin="lower",
    cmap=background_colourmap,
)

# Plot the contours on top of the background.
#     (Note: 'RuntimeWarning: invalid value encountered in...' is raised for
#      certain designs where e.g. division by zero is encountered, but this is
#      mathematically inevitable and often important in the resulting design.)
plt.contour(
    x,
    y,
    contour_function(x, y),
    linewidths=np.arange(*linewidth_parameters),
    cmap=contour_colourmap,
)

# Save and display the overall figure i.e. the full design in high resolution.
plt.savefig(
    "%s.png" % design_choice, format="png", bbox_inches="tight", dpi=1000
)
plt.show()
