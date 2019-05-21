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


# Colour scheme for designs without use of the advanced colouring module:
NO_COLOURING_DARK = 'darkkhaki'
NO_COLOURING_MID = 'palegoldenrod'  # of lightness between _DARK and _LIGHT
NO_COLOURING_LIGHT = 'lemonchiffon'
NO_COLOURING_TRANSPARENT = 'none'  # implies (by context) unfilled or no edges


""" Define data for all example designs in a single dictionary.

Dictionary keys are the design identifiers, which are simply labels of
'repolygon_design_i' for integer 'i'. In general, the higher the label value
of 'i', the more complicated the design with respect to the styling.

Dictionary values are the design's defining data which is stored in a
two-tuple data structure, with the first element a list of tiled (identical)
polygon layers (here labelled 'j') to plot, each defined as another two-tuple:

    (
     (A_j, B_j, C_j, (Dx_j, Dy_j), (Ex_j, Ey_j)),
     (F_j, G_j, H_j, I_j, J_j)
    )

where the elements of the first tuple define the geometry of the specific
polygon tile layer, and are (all being compulsory to define):

    * A_j :
        number of sides of the polygon e.g. 4 produces a square, 6 a hexagon;
    * B_j :
        size of the polygon, scaled relative to 1 for a polygon drawn on the
        unit circle (a circle of radius 1);
    * C_j :
        rotational factor x, which rotates the polygon by 180/x degrees
        relative to the equivalent polygon with a horizontal top edge;
    * Dx_j, Dy_j :
        tile-to-tile distance (take any vertex as a reference) along the 'x'
        (Dx_j) and 'y' (Dy_j) axes;
    * Ex_j, Ey_j :
        shift from 0 for the first polygon's root vertex 'x' (Ex_j) and 'y'
        (Ey_j) coordinates (this shift is also applied to all other polygons).

and the elements for the second tuple define the styling of that same layer,
and are (all being optional, with defaults as given applied if undefined):

    * F_j :
        linewidth of the edges (default 1);
    * G_j :
        style of edges (default 'solid');
    * H_j :
        colour of the edges (default NO_COLOURING_LIGHT);
    * I_j :
        colour of any fill (default NO_COLOURING_TRANSPARENT i.e. no fill);
    * J_j :
        integer influencing the order in which the tile layer is plotted
        relative to other layers (the matplotlib 'zorder'), where the higher
        the integer the further towards top the layer appears (default 0).

and the second element of the overarching two-tuple defines properties of the
whole design and is defined as:

    (
     (Kx_min, Kx_max, Ky_min, Ky_max),
     L
    )

where the elements of the above tuple are (where L is optional):

    * Kx_min, Kx_max :
        the 'x' axes limits i.e. minimum (Kx_min) & maximum (Kx_max) points
        which bound the full design i.e. plot;
    * Ky_min, Ky_max :
        the 'y' axes limits i.e. minimum (Ky_min) & maximum (Ky_max) points
        which bound the full design i.e. plot;
    * L :
        the background colour of the full design i.e. plot facecolour
        (default NO_COLOURING_DARK).

This gives an overall structure, indented consistently as follows for tuple
distinction and general clarity, for 'j = 1, 2, ..., n' tiled polygon layers:

    (
        [
            ((A_1, B_1, C_1, (Dx_1, Dy_1), (Ex_1, Ey_1)),
             (F_1, G_1, H_1, I_1, J_1)),
            ((A_2, B_2, C_2, (Dx_2, Dy_2), (Ex_2, Ey_2)),
             (F_2, G_2, H_2, I_2, J_2)),
                ...
                ...
                ...
            ((A_n, B_n, C_n, (Dx_n, Dy_n), (Ex_n, Ey_n)),
             (F_n, G_n, H_n, I_n, J_n)),
        ],
        ((Kx_min, Kx_max, Ky_min, Ky_max), L)
    )

"""
REPOLYGON_EXAMPLES = {
    "repolygon_design_1": (
        [
            ((4, 15.125, 1, (15, 48), (0, 0)),
             ()),
            ((6, 15.125, 1, (15, 48), (7.5, 24)),
             ()),
            ((12, 22, 12, (15, 48), (7.5, 24)),
             ()),
        ],
        ((40, 200, 40, 200),)),
    "repolygon_design_2": (
        [
            ((6, 2, 1, (12.2, 7), (0, 0)),
             ()),
            ((6, 2, 1, (12.2, 7), (6.1, 3.5)),
             ()),
            ((12, 6, 1, (12.2, 7), (0, 0)),
             ()),
            ((12, 6, 1, (12.2, 7), (6.1, 3.5)),
             ()),
            ((50, 3.5, 6, (12.2, 7), (0, 0)),
             ()),
            ((50, 3.5, 6, (12.2, 7), (6.1, 3.5)),
             ()),
        ],
        ((6.1, 42.7, 6.1, 42.7),)),
    "repolygon_design_3": (
        [
            ((4, 1, 1, (6, 6), (2, 2)),
             (0.75,)),
            ((6, 2, 1, (6, 6), (2, 2)),
             (0.75,)),
            ((6, 2.75, 1, (6, 6), (5, 5)),
             (0.75,)),
            ((8, 5, 1, (6, 6), (2, 2)),
             (0.75,)),
            ((12, 3.5, 1, (6, 6), (2, 2)),
             (0.75,)),
        ],
        ((2, 26, 2, 26),)),
    "repolygon_design_4": (
        [
            ((16, 0.9, 1, (6, 6), (0, 0)),
             (1.5,)),
            ((16, 0.9, 1, (6, 6), (3, 3)),
             (1.5,)),
            ((16, 0.9, 8, (6, 6), (0, 0)),
             (1.5,)),
            ((16, 0.9, 8, (6, 6), (3, 3)),
             (1.5,)),
            ((16, 1.8, 1, (6, 6), (0, 0)),
             (3,)),
            ((16, 1.8, 1, (6, 6), (3, 3)),
             (3,)),
            ((16, 1.8, 8, (6, 6), (0, 0)),
             (3,)),
            ((16, 1.8, 8, (6, 6), (3, 3)),
             (3,)),
            ((16, 2.7, 1, (6, 6), (0, 0)),
             (4.5,)),
            ((16, 2.7, 1, (6, 6), (3, 3)),
             (5.5,)),
            ((16, 2.7, 8, (6, 6), (0, 0)),
             (4.5,)),
            ((16, 2.7, 8, (6, 6), (3, 3)),
             (4.5,)),
            ((16, 3.6, 1, (6, 6), (0, 0)),
             (6,)),
            ((16, 3.6, 1, (6, 6), (3, 3)),
             (6,)),
            ((16, 3.6, 8, (6, 6), (0, 0)),
             (6,)),
            ((16, 3.6, 8, (6, 6), (3, 3)),
             (6,)),
        ],
        ((6, 24, 6, 24),)),
    "repolygon_design_5": (
        [
            ((8, 1.6, 8, (4, 4), (0, 0)),
             (3,)),
            ((8, 2.5, 1, (4, 4), (0, 0)),
             (2,)),
            ((8, 4, 1, (4, 4), (0, 0)),
             (2,)),
        ],
        ((0, 20, 0, 20),)),
    "repolygon_design_6": (
        [
            ((4, 1.28, -2.58, (5.6, 5.6), (0, 0)),
             (2,)),
            ((8, 8.5, 4.25, (5.6, 5.6), (0, 0)),
             (6,)),
            ((8, 10, 4.25, (5.6, 5.6), (0, 0)),
             (2,)),
        ],
        ((11.2, 28, 11.2, 28),)),
    "repolygon_design_7": (
        [
            ((12, 0.56, -2.8, (5.6, 5.6), (0, 0)),
             (7,)),
            ((12, 1.4, -2.8, (5.6, 5.6), (0, 0)),
             (6,)),
            ((12, 2.24, -2.8, (5.6, 5.6), (0, 0)),
             (5,)),
            ((12, 3.08, -2.8, (5.6, 5.6), (0, 0)),
             (4,)),
            ((12, 3.92, -2.8, (5.6, 5.6), (0, 0)),
             (3,)),
            ((12, 4.72, -2.8, (5.6, 5.6), (0, 0)),
             (2,)),
            ((12, 5.6, -2.8, (5.6, 5.6), (0, 0)),
             ()),
        ],
        ((2.8, 19.6, 2.8, 19.6),)),
    "repolygon_design_8": (
        [
            ((4, 0.45, 1, (5.6, 5.6), (0, 2.8)),
             ()),
            ((4, 0.7, 1, (5.6, 5.6), (0, 2.8)),
             ()),
            ((6, 0.8, 6, (5.6, 5.6), (2.8, 0)),
             ()),
            ((6, 1, 6, (5.6, 5.6), (2.8, 0)),
             ()),
            ((6, 1.8, 6, (5.6, 5.6), (0, 0)),
             ()),
            ((6, 2, 6, (5.6, 5.6), (0, 0)),
             ()),
            ((12, 7.8, 12, (5.6, 5.6), (0, 0)),
             ()),
            ((12, 8, 12, (5.6, 5.6), (0, 0)),
             ()),
        ],
        ((2.8, 19.6, 2.8, 19.6),)),
    "repolygon_design_9": (
        [
            ((4, 0.7, 4, (8, 8), (2, 2)),
             ()),
            ((4, 1.1, 4, (8, 8), (2, 2)),
             ()),
            ((8, 1.7, 1, (4, 4), (0, 0)),
             ()),
            ((8, 2.0, 1, (4, 4), (0, 0)),
             ()),
            ((12, 5.7, 12, (8, 8), (2, 2)),
             ()),
            ((12, 6.0, 12, (8, 8), (2, 2)),
             ()),
        ],
        ((4, 24, 4, 24),)),
    "repolygon_design_10": (
        [
            ((4, 1, 1, (8, 8), (0, 4)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 1)),
            ((4, 1, 1, (8, 8), (4, 0)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 2)),
            ((4, 2.5, 1, (8, 8), (0, 0)),
             (10, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 9)),
            ((4, 2.5, 1, (8, 8), (4, 4)),
             (10, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 5)),
            ((4, 2.5, 4, (8, 8), (0, 0)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 10)),
            ((4, 2.5, 4, (8, 8), (4, 4)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 6)),
            ((4, 3, 1, (8, 8), (0, 0)),
             (10, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 7)),
            ((4, 3, 1, (8, 8), (4, 4)),
             (10, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_MID, 3)),
            ((4, 3, 4, (8, 8), (0, 0)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 8)),
            ((4, 3, 4, (8, 8), (4, 4)),
             (3, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_MID, 4)),
            ((8, 3, 1, (8, 8), (4, 4)),
             (10, 'solid', NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 0)),
        ],
        ((4, 36, 4, 36), NO_COLOURING_MID)),
    "repolygon_design_11": (
        [
            ((6, 8, 6, (13.86, 24), (0, 0)),
             (2.5, 'dashed', NO_COLOURING_DARK, NO_COLOURING_TRANSPARENT, 11)),
            ((6, 8, 6, (13.86, 24), (0, 0)),
             (9, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_MID, 0)),
            ((6, 8, 6, (13.86, 24), (6.93, 12)),
             (2.5, 'dashed', NO_COLOURING_DARK, NO_COLOURING_TRANSPARENT, 4)),
            ((6, 8, 6, (13.86, 24), (6.93, 12)),
             (9, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 1)),
            ((50, 1.8, 6, (13.86, 24), (0, 0)),
             (1.5, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 10)),
            ((50, 1.8, 6, (13.86, 24), (6.93, 12)),
             (1.5, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 7)),
            ((50, 3.1, 6, (13.86, 24), (0, 0)),
             (2.5, 'dotted', NO_COLOURING_DARK, NO_COLOURING_TRANSPARENT, 8)),
            ((50, 3.1, 6, (13.86, 24), (0, 0)),
             (7, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 3)),
            ((50, 3.1, 6, (13.86, 24), (6.93, 12)),
             (2.5, 'dotted', NO_COLOURING_MID, NO_COLOURING_TRANSPARENT, 5)),
            ((50, 3.1, 6, (13.86, 24), (6.93, 12)),
             (7, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 2)),
            ((50, 4.4, 6, (13.86, 24), (0, 0)),
             (1.5, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 9)),
            ((50, 4.4, 6, (13.86, 24), (6.93, 12)),
             (1.5, 'solid', NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 6)),

        ],
        ((0.0, 55.44, 3.5, 57.94), NO_COLOURING_DARK)),
}


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
