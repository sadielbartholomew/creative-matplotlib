"""Polar views of simulated Brownian motion resembling spinning yarn."""

import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt
from matplotlib import rcParams


# ---------- Spindle parameters ---------
# Path parameters

T = 300  # overall time under brownian motion to simulate
n = 250  # total number of revolutions to simulate
N = 10000  # total number of path steps
variance_parameter = 0.5  # sq. root of the random variable variance over time

# Output plot colour choices
background_colour = "#14001B"  # off-black
plot_spindles_with_colours = [
    "bone",
    "twilight",
    "cividis",
    "gist_earth",
    "pink",
    "ocean",
    "terrain",
    "copper",
    "OrRd",
]
# ---------------------------------------


def simulate_brownian_motion(
    initial_pos, total_steps, time_step, variance_parameter, path
):
    """TODO."""
    initial_pos = np.asarray(initial_pos)
    scale_factor = variance_parameter * np.sqrt(time_step)
    random_variates = norm.rvs(
        size=initial_pos.shape + (total_steps,), scale=scale_factor
    )
    np.cumsum(random_variates, axis=-1, out=path)
    path += np.expand_dims(initial_pos, axis=-1)

    return path


def plot_spool_of_brownian_motion(ax):
    """TODO."""
    path_array = np.zeros((n, N + 1))
    simulate_brownian_motion(
        path_array[:, 0], N, T / N, variance_parameter, path=path_array[:, 1:]
    )
    time_step = np.linspace(0.0, T, N + 1)

    return (time_step, path_array)


def create_formatted_figure():
    """TODO."""
    side_size = min(*rcParams["figure.figsize"])
    fig = plt.figure(figsize=(side_size, side_size))
    fig.tight_layout()
    fig.patch.set_facecolor(background_colour)

    ax = plt.subplot(projection="polar")
    ax.spines["polar"].set_visible(False)
    ax.set_rmax(5)
    ax.set_xticks([])
    ax.set_rticks([])
    ax.set_aspect("equal")
    ax.set_facecolor(background_colour)

    return fig, ax


# Plot examples in varying colourmaps:
for colourmap in plot_spindles_with_colours:
    fig, axes = create_formatted_figure()
    t, r = plot_spool_of_brownian_motion(axes)

    foreground_colourmap = getattr(plt.cm, colourmap)(np.linspace(0, 1, n))
    for index in range(n):
        axes.plot(
            t,
            r[index],
            alpha=0.2,
            linewidth=0.2,
            color=foreground_colourmap[index],
        )

    # Show and save the final output
    fig.savefig(f"outputs/spindles-instance-in-{colourmap}.png", dpi=1200)
    plt.show()
