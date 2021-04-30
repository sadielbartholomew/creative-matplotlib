"""**repolygon**: create designs by spatial *re*petition of *polygon*s.

Created by Sadie Bartholomew, 2017; tidied & uploaded to GitHub 2019.

Version 0.2:
    - Includes:
        - core code for creating a (two/three-tone) tiling design with
          polygons, including eleven example designs generated in turn from
          the raw code
        - option to ignore any number of vertices so they are not plotted,
          giving an open partial polygon as the basic patch to repeat, with an
          example design which replicates the iconic carpet from Kubrick's
          film 'The Shining' and produces a variant with different colours.
    - Excludes:
        modules for advanced colouring including according to patch
        intersections, & for incorporating curved variants of polygons, with
        further examples making use of these extra modules.
"""

import copy
from itertools import product as iproduct
from matplotlib import patches as mpatches, path as mpath, pyplot as plt
import numpy as np

from repolygon_example_designs import (
    NO_COLOURING_DARK,
    NO_COLOURING_MID,
    NO_COLOURING_LIGHT,
    NO_COLOURING_TRANSPARENT,
    FULL_COLOUR_EXAMPLES_COLOURS,
    MINIMAL_TONE_EXAMPLES_SPEC,
    FULL_COLOUR_EXAMPLES_SPEC,
    CARPET_KUBRICK_THE_SHINING_COLOURS,
    CARPET_KUBRICK_THE_SHINING_SPEC,
)

NO_COLOURING_SCHEME = (
    NO_COLOURING_DARK,
    NO_COLOURING_MID,
    NO_COLOURING_LIGHT,
    NO_COLOURING_TRANSPARENT,
)


class tileLayer:
    """Determines coordinates for a single repeated polygon layer."""

    def __init__(self, n_sides, scale, rotation_no, xy_additions, xy_shifts):
        """Set up a new tile layer."""
        self.draw_path = mpath.Path

        self.n_sides = n_sides
        self.scale = scale
        self.rotation_no = rotation_no
        self.xy_additions = xy_additions
        self.xy_shifts = xy_shifts

    @staticmethod
    def transform_coors(factor):
        """Create a vector for rotating coordinates about the origin."""
        return np.array([np.cos(factor), np.sin(factor)])

    def ngon_vertex(self, xy_increases, vertex_i):
        """Find coordinates for one vertex of the n-gon to repeat."""
        # If factorise out np.pi below, get a different result: why!?
        transform = (
            2 * vertex_i * np.pi / self.n_sides + np.pi / self.rotation_no
        )
        ngon_xy = (
            self.scale * self.transform_coors(transform)
            + np.array(xy_increases) * np.array(self.xy_additions)
            + np.array(self.xy_shifts)
        )
        return ngon_xy

    def ngon_coors(self, xy_increases, ignore_n_vertices=False):
        """Find coordinates for all vertices of the n-gon to tile."""
        newpath_data = [
            (self.draw_path.MOVETO, self.ngon_vertex(xy_increases, 0))
        ]

        # Manage how many vertices to plot for each patch, usually all:
        loop_over_vertices = self.n_sides + 2
        if ignore_n_vertices:
            # Add two here and above to cover final vertex and point to close
            loop_over_vertices -= ignore_n_vertices + 2
        # Loop to n_sides *+1* so polygon closes properly, else get small gap:
        for vertex in range(1, loop_over_vertices):
            newpath_data.append(
                (self.draw_path.LINETO, self.ngon_vertex(xy_increases, vertex))
            )
        if not ignore_n_vertices:  # do not close in this case.
            newpath_data.append(
                (self.draw_path.CLOSEPOLY, self.ngon_vertex(xy_increases, 0))
            )
        return newpath_data

    def ngon_layer_coors(
        self,
        linewidth=1,
        linestyling="solid",
        colour=NO_COLOURING_LIGHT,
        fill_colour=NO_COLOURING_TRANSPARENT,
        zorder_var=0,
        repeats=20,
        ignore_n_vertices=False,
    ):
        """Find coordinates for all vertices of all the tiled n-gons."""
        patches = []
        for x_inc, y_inc in iproduct(range(repeats), range(repeats)):
            codes, verts = zip(
                *self.ngon_coors(
                    (x_inc, y_inc), ignore_n_vertices=ignore_n_vertices
                )
            )
            specific_draw_path = mpath.Path(verts, codes)
            patch = mpatches.PathPatch(
                specific_draw_path,
                linewidth=linewidth,
                linestyle=linestyling,
                edgecolor=colour,
                facecolor=fill_colour,
                zorder=zorder_var,
            )
            patches.append(patch)
        return patches


class plottedDesign:
    """Plot sets of repeated polygon layers on a single canvas."""

    def __init__(self, all_tile_layers, colour_scheme=None):
        """Set up a new repolygon plot of repeated polygon layers."""
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.fig.set_canvas(plt.gcf().canvas)
        plt.xticks([])
        plt.yticks([])

        self.all_tile_layers = all_tile_layers
        self.colour_scheme = colour_scheme

    @staticmethod
    def colour_intersection(
        patch_1, patch_2, intersection_colour, new_zorder=-100
    ):
        """Colour the spatial intersection between two given patches."""
        # Create copies of each patch. Colour one, leaving other transparent.
        intersection_patch = copy.copy(patch_2)
        intersection_patch.set_facecolor(intersection_colour)
        clip_patch = copy.copy(patch_1)
        clip_patch.set_fill(False)

        # Set the zorder so that intersection patch is on top of the original:
        zorder_orig = intersection_patch.get_zorder()
        intersection_patch.set_zorder(zorder_orig + new_zorder)
        return (intersection_patch, clip_patch)

    def get_all_tile_data(self, tile_layer_set):
        """Get geometry and style for all repeated polygon layers."""
        all_points = []
        for tile_layer in tile_layer_set:
            tile_coors, tile_style = tile_layer
            if self.colour_scheme:
                use_style = list(tile_style)
                if (
                    len(tile_style) > 2
                    and tile_style[2] not in NO_COLOURING_SCHEME
                ):
                    use_style[2] = self.colour_scheme[tile_style[2]]
                if (
                    len(tile_style) > 3
                    and tile_style[3] not in NO_COLOURING_SCHEME
                ):
                    use_style[3] = self.colour_scheme[tile_style[3]]
            else:
                use_style = tile_style

            tile_design = tileLayer(*tile_coors)
            all_points.append(tile_design.ngon_layer_coors(*use_style))
        return all_points

    def draw_all_tiles(
        self, filename, cutoffs, facecolour=NO_COLOURING_DARK, col_int=None
    ):
        """Plot all layers on a canvas with given region and colour."""
        # Set-up the matplotlib canvas according to preferences.
        self.ax.set_aspect(1)
        if self.colour_scheme and facecolour not in NO_COLOURING_SCHEME:
            facecolour = self.colour_scheme[facecolour]
        self.ax.set_facecolor(facecolour)
        plt.axis(cutoffs)

        # Draw all tile layers in the design polygon patch by polygon patch.
        all_stuff = self.get_all_tile_data(self.all_tile_layers)

        if not col_int:
            col_int = []
        for col_i in col_int:
            for index, tile_layer in enumerate(all_stuff):
                # Colour intersections:
                if index == col_i[0]:
                    save_patch_0 = tile_layer
                if index == col_i[1]:
                    save_patch_1 = tile_layer
            for patch_0, patch_1 in zip(save_patch_0, save_patch_1):
                # if col_int only:
                if self.colour_scheme:
                    use_colour = self.colour_scheme[col_i[2]]
                self.ax.add_patch(
                    self.colour_intersection(
                        patch_0, patch_1, use_colour, col_i[3]
                    )[0]
                )

        for tile_layer_patches in all_stuff:
            for tile_layer_patch in tile_layer_patches:
                self.ax.add_patch(tile_layer_patch)

        # Save and display the overall design on the canvas.
        self.fig.savefig(
            "designs/" + filename + ".png",
            format="png",
            bbox_inches="tight",
            transparent=False,
            dpi=1000,
        )
        plt.show()


# Render and save a set of original designs:
for example_name, example_data in MINIMAL_TONE_EXAMPLES_SPEC.items():
    filename = example_name + "_minimal_tone"
    plottedDesign(example_data[0]).draw_all_tiles(filename, *example_data[1])

for example_name, example_data in FULL_COLOUR_EXAMPLES_SPEC.items():
    filename = example_name + "_full_colour"
    plot_comp_0, plot_comp_1, plot_comp_2 = example_data
    plottedDesign(
        plot_comp_0, FULL_COLOUR_EXAMPLES_COLOURS[example_name]
    ).draw_all_tiles(filename, *plot_comp_2, col_int=plot_comp_1)

# Also recreate and save the iconic carpet from the Kubrick film 'The Shining':
directory = "carpet_kubrick_the_shining"
spec = CARPET_KUBRICK_THE_SHINING_SPEC
colours = CARPET_KUBRICK_THE_SHINING_COLOURS
# Plot actual design as well as an alternative design with different colours
for design in ("ACTUAL_DESIGN", "ALTERNATIVE_COLOUR_DESIGN"):
    id_to_append = design.split("_")[0].lower()
    plottedDesign(spec[design][0], colours[design]).draw_all_tiles(
        f"{directory}/{directory}_{id_to_append}", *spec[design][1]
    )
