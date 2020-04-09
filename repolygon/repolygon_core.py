"""
**Repolygon**: create intricate tiling designs from *re*peated *polygon*
               matplotlib patches.

Created by Sadie Bartholomew, 2017; tidied & uploaded to GitHub 2019.

Version 0.1:
    - Includes:
        core code for creating a (two/three-tone) tiling design with polygons,
        including eleven example designs generated in turn from the raw code.
    - Excludes:
        modules for advanced colouring including according to patch
        intersections, & for incorporating curved variants of polygons, with
        further examples making use of these extra modules.
"""

from itertools import product as iproduct
from matplotlib import patches as mpatches, path as mpath, pyplot as plt
import numpy as np

from repolygon_example_designs import (
    REPOLYGON_EXAMPLES,
    REPOLYGON_EXAMPLES_COLOURS,
    NO_COLOURING_DARK,
    NO_COLOURING_MID,
    NO_COLOURING_LIGHT,
    NO_COLOURING_TRANSPARENT
)


class tileLayer():
    """ Determines coordinates for a single tiled (repeated) polygon layer. """

    def __init__(self, n_sides, scale, rotation_no, xy_additions, xy_shifts):
        self.draw_path = mpath.Path

        self.n_sides = n_sides
        self.scale = scale
        self.rotation_no = rotation_no
        self.xy_additions = xy_additions
        self.xy_shifts = xy_shifts

    @staticmethod
    def transform_coors(factor):
        """ Create a vector for rotating coordinates about the origin. """
        return np.array([np.cos(factor), np.sin(factor)])

    def ngon_vertex(self, xy_increases, vertex_i):
        """ Find coordinates for one vertex ('_i') of the n-gon to tile. """
        # If factorise out np.pi below, get a different result: why!?
        transform = 2 * vertex_i * np.pi/self.n_sides + np.pi/self.rotation_no
        ngon_xy = (self.scale * self.transform_coors(transform) +
                   np.array(xy_increases) * np.array(self.xy_additions) +
                   np.array(self.xy_shifts))
        return ngon_xy

    def ngon_coors(self, xy_increases):
        """ Find coordinates for all vertices of the n-gon to tile. """
        newpath_data = [(self.draw_path.MOVETO,
                         self.ngon_vertex(xy_increases, 0))]
        # Loop to n_sides *+1* so polygon closes properly, else get small gap:
        for vertex in range(1, self.n_sides + 2):
            newpath_data.append((
                self.draw_path.LINETO, self.ngon_vertex(xy_increases, vertex)))
        newpath_data.append((
            self.draw_path.CLOSEPOLY,
            self.ngon_vertex(xy_increases, 0)))
        return newpath_data

    def ngon_layer_coors(
            self, linewidth=1, linestyling='solid', colour=NO_COLOURING_LIGHT,
            fill_colour=NO_COLOURING_TRANSPARENT, zorder_var=0, repeats=20):
        """ Find coordinates for all vertices of all the tiled n-gons. """
        patches = []
        for x_inc, y_inc in iproduct(range(repeats), range(repeats)):
            codes, verts = zip(*self.ngon_coors((x_inc, y_inc)))
            specific_draw_path = mpath.Path(verts, codes)
            patch = mpatches.PathPatch(
                specific_draw_path, linewidth=linewidth, linestyle=linestyling,
                edgecolor=colour, facecolor=fill_colour, zorder=zorder_var)
            patches.append(patch)
        return patches


class plottedDesign():
    """ Plots sets of tiled (repeated) polygon layers on a single canvas. """

    def __init__(self, all_tile_layers):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.fig.set_canvas(plt.gcf().canvas)
        plt.xticks([])
        plt.yticks([])

        self.all_tile_layers = all_tile_layers

    @staticmethod
    def get_all_tile_data(tile_layer_set):
        """ Extract data (geometry & style) for all tiled polygon layers. """
        all_points = []
        for tile_layer in tile_layer_set:
            tile_coors, tile_style = tile_layer
            tile_design = tileLayer(*tile_coors)
            all_points.append(tile_design.ngon_layer_coors(*tile_style))
        return all_points

    def draw_all_tiles(self, filename, cutoffs, facecolour=NO_COLOURING_DARK):
        """ Plot all layers on a single canvas of set region and colour. """
        # Set-up the matplotlib canvas according to preferences.
        self.ax.set_aspect(1)
        self.ax.set_facecolor(facecolour)
        plt.axis(cutoffs)

        # Draw all tile layers in the design polygon patch by polygon patch.
        for tile_layer_patches in self.get_all_tile_data(self.all_tile_layers):
            for tile_layer_patch in tile_layer_patches:
                self.ax.add_patch(tile_layer_patch)

        # Save and display the overall design on the canvas.
        self.fig.savefig('designs/' + filename, format='png',
                         bbox_inches='tight', transparent=False, dpi=1000)
        plt.show()


for example_name, example_data in REPOLYGON_EXAMPLES.items():
    filename = example_name + '.png'
    plottedDesign(example_data[0]).draw_all_tiles(
        filename, *example_data[1])
