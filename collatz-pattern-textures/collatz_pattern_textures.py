"""Graphic designs based on a plot concerning the Collatz conjecture.

Original graphic texture designs all generated with the scatter pattern of
the plot of the number of iterations required for convergence to one in the
Collatz conjecture (also known as the `3n + 1` conjecture and by other names),
where the pattern has been plotted at some transparency level multiple times,
each plot shifted linearly and translated, both by a small amount, relative
to the other plots.

(For detail on the Collatz conjecture and the plot in question, see, e.g:

* https://mathworld.wolfram.com/CollatzProblem.html
* https://www.quantamagazine.org/
      why-mathematicians-still-cant-solve-the-collatz-conjecture-20200922/
* https://en.wikipedia.org/wiki/Collatz_conjecture

including the following GIF which shows the plot at several scales:

* https://en.wikipedia.org/wiki/File:Collatz_Gif.gif
)

Note that no randomness is used in these designs; each has been curated from
the plot pattern by applying chosen, static, values for the:

* number of scatter plots to use and the relative shifts between them;
* plot limiting bounds i.e. the window on the overall figure to view;
* marker size and transparency, consistent across each individual figure;
* colours used for the background and for the various plot sets in each figure.


Created by Sadie L. Bartholomew, February 2021.

"""

import matplotlib.pyplot as plt

from itertools import cycle


# Define three colour schemes to use across all nine designs (three uses each)
BACKGROUND_COL_1 = "#452145"  # dark purple
FOREGOUND_COLOURS_1 = cycle(
    [
        "#372248",  # lighter purple
        "#5B85AA",  # purple-blue
        "#414770",  # navy blue mix
        "#2F9C95",  # viridian green
        "#40C9A2",  # another green
        "#E5F9E0",  # pale grey
    ]
)

BACKGROUND_COL_2 = "#0C0C0C"  # grey
FOREGOUND_COLOURS_2 = cycle(
    [
        "#78E0DC",  # light turquoise
        "#276FBF",  # mid blue
        "#5C80BC",  # grey-blue
        "#FFEEE2",  # linen
        "#FFFD77",  # lemon
        "#E26D5A",  # terracotta
    ]
)

BACKGROUND_COL_3 = "#751A2E"  # claret
FOREGOUND_COLOURS_3 = cycle(
    [
        "#126E46",  # forest green
        "#071836",  # navy
        "#0353A4",  # blue
        "#8CB369",  # light olive
        "#F4D35E",  # yellow
        "#F05D5E",  # pink-red
    ]
)


PATTERN_SHIFT_1 = [
    (1, 0),
    (1.1, -5),
    (0.89, -2),
    (0.95, -20),
    (0.99, 4),
    (0.9, 12),
]
PATTERN_SHIFT_2 = [
    (0.96, 10),
    (1.15, -3),
    (0.98, 5),
    (1.03, 0),
    (0.94, -10),
    (1, 3),
]
PATTERN_SHIFT_3 = [
    (1.03, -12),
    (0.91, +10),
    (1, -10),
    (0.95, -20),
    (1.2, -50),
    (0.99, 0),
]


WINDOW_1 = ((7000, 21000), (10, 160))
WINDOW_2 = ((5000, 18000), (110, 190))
WINDOW_3 = ((1750, 20000), (5, 170))


def collatz():
    """TODO."""
    steps = []
    for n in range(1, 50000):
        count = 0
        while not n == 1:
            if n % 2 == 0:
                n /= 2
            else:
                n = 3 * n + 1
            count += 1
        steps.append(count)

    return steps


def shift_sequence(seq, m, c):
    """TODO."""
    return [m * x + c for x in seq]


def create_formatted_figure(xy_limits, background_col):
    """TODO."""
    fig = plt.figure(figsize=(6, 6))
    fig.tight_layout()
    fig.patch.set_facecolor(background_col)

    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(xy_limits[0])
    ax.set_ylim(xy_limits[1])
    ax.set_facecolor(background_col)

    return fig, ax


def create_and_save_design(
    seq,
    index,
    pattern_shifts,
    xy_limits,
    background_col,
    foreground_cols,
    marker_type,
    marker_size,
    marker_alpha,
):
    """TODO."""
    fig, axes = create_formatted_figure(xy_limits, background_col)
    for pattern_shift in pattern_shifts:
        axes.plot(
            shift_sequence(seq, *pattern_shift),
            marker_type,
            color=next(foreground_cols),
            markersize=marker_size,
            alpha=marker_alpha,
        )
    fig.savefig(f"collatz_textile_{index}.png", bbox_inches="tight", dpi=600)


# For efficiency, calculate this only once, to re-use, since it is static.
collatz_iterations = collatz()

# Design 1: dense, in purple and green colour scheme.
create_and_save_design(
    collatz_iterations,
    1,
    PATTERN_SHIFT_1,
    WINDOW_1,
    BACKGROUND_COL_1,
    FOREGOUND_COLOURS_1,
    "v",
    8,
    0.05,
)

# Design 2: sparser in black and bold colours.
create_and_save_design(
    collatz_iterations,
    2,
    PATTERN_SHIFT_3,
    WINDOW_3,
    BACKGROUND_COL_2,
    FOREGOUND_COLOURS_2,
    "v",
    6,
    0.02,
)

# Design 3: sparsest in blue, red, green and yellow on maroon colour scheme.
create_and_save_design(
    collatz_iterations,
    3,
    PATTERN_SHIFT_2,
    WINDOW_2,
    BACKGROUND_COL_3,
    FOREGOUND_COLOURS_3,
    "v",
    8,
    0.05,
)

# Design 4: oversize markers giving blur effect: crosses.
create_and_save_design(
    collatz_iterations,
    4,
    PATTERN_SHIFT_3,
    WINDOW_3,
    BACKGROUND_COL_2,
    FOREGOUND_COLOURS_2,
    "X",
    11,
    0.03,
)

# Design 5: oversize markers giving blur effect: square markers.
create_and_save_design(
    collatz_iterations,
    5,
    PATTERN_SHIFT_2,
    WINDOW_2,
    BACKGROUND_COL_3,
    FOREGOUND_COLOURS_3,
    "s",
    15,
    0.03,
)

# Design 6: oversize markers giving blur effect: rotated square.
create_and_save_design(
    collatz_iterations,
    6,
    PATTERN_SHIFT_1,
    WINDOW_1,
    BACKGROUND_COL_1,
    FOREGOUND_COLOURS_1,
    "D",
    18,
    0.03,
)

# Design 7: very transparent with many shifts and oversized markers too.
create_and_save_design(
    collatz_iterations,
    7,
    PATTERN_SHIFT_1 + PATTERN_SHIFT_2 + PATTERN_SHIFT_3,
    ((9850, 10900), (27, 79)),
    BACKGROUND_COL_2,
    FOREGOUND_COLOURS_2,
    "x",
    30,
    0.04,
)

# Design 8: ditto to above, but the markers aren't as oversized.
create_and_save_design(
    collatz_iterations,
    8,
    PATTERN_SHIFT_1 + PATTERN_SHIFT_2 + PATTERN_SHIFT_3,
    ((13500, 15500), (20, 80)),
    BACKGROUND_COL_3,
    FOREGOUND_COLOURS_3,
    "H",
    20,
    0.03,
)

# Design 9: many scatter patterns but only slighty transparent markers giving
# a paint-smudge-like effect.
create_and_save_design(
    collatz_iterations,
    9,
    PATTERN_SHIFT_1 + PATTERN_SHIFT_2 + PATTERN_SHIFT_3,
    ((13000, 19000), (10, 80)),
    BACKGROUND_COL_1,
    FOREGOUND_COLOURS_1,
    "4",
    18,
    0.4,
)


plt.show()
