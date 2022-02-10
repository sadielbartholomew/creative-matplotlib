import matplotlib.pyplot as plt

from itertools import cycle


BACKGROUND_COL = "#02040F" 
FOREGOUND_COLOURS = [
    "#E59500",  # bright yellow
    "#002642",  # navy
    "#840032",  # maroon
    "#CFD11A",  # pear
    "#FFB4A2",  # coral
    "#AFA2FF",  # bright lilac
]
stage_two_colour_selector = cycle(FOREGOUND_COLOURS)


def collatz():
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


def create_formatted_figure(background_col):
    """TODO."""
    fig = plt.figure(figsize=(6, 6))
    #fig.tight_layout()
    fig.patch.set_facecolor(background_col)

    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim([10000, 20000])
    ax.set_ylim([50, 100])
    ax.set_facecolor(background_col)

    return fig, ax


fig, axes = create_formatted_figure(BACKGROUND_COL)
for pattern_shift in [
        (1, 0),
        (1.1, -5),
        (0.89, -2),
        (0.95, -20),
        (0.99, 4),
        (0.9, 12),
]:
    axes.plot(
        shift_sequence(collatz(), *pattern_shift), "v",
        color=next(stage_two_colour_selector), markersize=8, alpha=0.05
    )

fig.savefig("collatz_textile.png", bbox_inches="tight", dpi=600)
plt.show()
