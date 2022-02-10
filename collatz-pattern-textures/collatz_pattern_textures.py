import matplotlib.pyplot as plt

from itertools import cycle


# Define three colour schemes to ues:
BACKGROUND_COL_1 =  "#452145"  # dark purple
FOREGOUND_COLOURS_1 = cycle(
    [
        "#372248",  # lighter purple
        "#5B85AA",  # purply blue
        "#414770",  # navy blue mix
        "#2F9C95",  # viridian green
        "#40C9A2",  # caribean green
        "#E5F9E0",  # pale grey
    ]
)

BACKGROUND_COL_2 = "#0C0C0C"  # grey
FOREGOUND_COLOURS_2 = cycle(
    [
        "#78E0DC",  # light turqouise
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


# Design 1: dense, in purple and green colour scheme
fig, axes = create_formatted_figure(
    ([7000, 21000], [10, 160]), BACKGROUND_COL_1)
for pattern_shift in [
    (1, 0), (1.1, -5), (0.89, -2), (0.95, -20), (0.99, 4), (0.9, 12),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "v",
        color=next(FOREGOUND_COLOURS_1), markersize=8, alpha=0.05
    )

fig.savefig("collatz_textile_1.png", bbox_inches="tight", dpi=600)


# Design 2: sparser in black and bold colours
fig, axes = create_formatted_figure(
    ([1750, 20000], [5, 170]), BACKGROUND_COL_2)
for pattern_shift in [
    (1.03, -12), (0.91, +10), (1, -10), (0.95, -20), (1.2, -50), (0.99, 0),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "v",
        color=next(FOREGOUND_COLOURS_2), markersize=6, alpha=0.02
    )

fig.savefig("collatz_textile_2.png", bbox_inches="tight", dpi=600)


# Design 3: sparsest in blue, red, green and yellow on maroon colour scheme
fig, axes = create_formatted_figure(
    ([5000, 18000], [110, 190]), BACKGROUND_COL_3)
for pattern_shift in [
    (0.96, 10), (1.15, -3), (0.98, 5), (1.03, 0), (0.94, -10), (1, 3),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "v",
        color=next(FOREGOUND_COLOURS_3), markersize=8, alpha=0.05
    )

fig.savefig("collatz_textile_3.png", bbox_inches="tight", dpi=600)


# Design 4: oversize markers giving blur effect: crosses.
fig, axes = create_formatted_figure(
    ([1750, 20000], [5, 170]), BACKGROUND_COL_2)
for pattern_shift in [
    (1.03, -12), (0.91, +10), (1, -10), (0.95, -20), (1.2, -50), (0.99, 0),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "X",
        color=next(FOREGOUND_COLOURS_2), markersize=11, alpha=0.03
    )

fig.savefig("collatz_textile_4.png", bbox_inches="tight", dpi=600)


# Design 5: oversize markers giving blur effect: square markers.
fig, axes = create_formatted_figure(
    ([5000, 18000], [110, 190]), BACKGROUND_COL_3)
for pattern_shift in [
    (0.96, 10), (1.15, -3), (0.98, 5), (1.03, 0), (0.94, -10), (1, 3),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "s",
        color=next(FOREGOUND_COLOURS_3), markersize=15, alpha=0.03
    )

fig.savefig("collatz_textile_5.png", bbox_inches="tight", dpi=600)


# Design 6: oversize markers giving blur effect: rotated square.
fig, axes = create_formatted_figure(
    ([7000, 21000], [10, 160]), BACKGROUND_COL_1)
for pattern_shift in [
    (1, 0), (1.1, -5), (0.89, -2), (0.95, -20), (0.99, 4), (0.9, 12),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "D",
        color=next(FOREGOUND_COLOURS_1), markersize=18, alpha=0.03
    )

fig.savefig("collatz_textile_6.png", bbox_inches="tight", dpi=600)


# Show all
plt.show()
