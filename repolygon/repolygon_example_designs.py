"""**repolygon**: create designs by spatial *re*petition of *polygon*s.

Created by Sadie Bartholomew, 2017; tidied & uploaded to GitHub 2019.

This module contains the data that defines the original example designs as
well as some replications of famous designs.

"""


# Colour scheme for designs without use of the advanced colouring module:
NO_COLOURING_DARK = "midnightblue"
NO_COLOURING_MID = "royalblue"  # of lightness between _DARK and _LIGHT
NO_COLOURING_LIGHT = "cornflowerblue"
NO_COLOURING_TRANSPARENT = "none"  # implies (by context) unfilled or no edges


""" Define colours for all example designs in a single dictionary.

Dictionary keys are the design identifiers, which are simply labels of
'repolygon_design_i' for integer 'i', and correspond to the designs
represented (with basic default colouring so as to distinguish the outlines)
in REPOLYGON_EXAMPLES.

Dictionary values are the design's defining colour set which is stored in a
dictionary structure where the keys are descriptors of each colour and the
values are the corresponding HTML colour codes specifying the exact colour.
"""
FULL_COLOUR_EXAMPLES_COLOURS = {
    "repolygon_design_1": {
        "BLACK": "#000000",
        "WHITE": "#FFFFFF",
        "DARK BLUE": "#2C254F",
        "LIGHT BLUE": "#617E83",
        "DARK BROWN": "#321D1C",
        "LIGHT BROWN": "#55423F",
    },
    "repolygon_design_2": {
        "OFF WHITE": "#DEF7FF",
        "BLUE": "#8788B9",
        "TEAL": "#232A31",
        "MINT": "#C6D2B6",
        "DARK BROWN": "#321E1E",
        "MEDIUM BROWN": "#662B1E",
        "SAND": "#AC9371",
    },
    "repolygon_design_3": {
        "OFF BLACK": "#080303",
        "GREY": "#2E2830",
        "DARK PURPLE": "#2B1931",
        "LIGHT PURPLE": "#604980",
        "DARK RED": "#611E15",
        "MEDIUM RED": "#8C2B23",
        "LIGHT RED": "#B93B2F",
        "DARK BROWN": "#30130D",
        "MEDIUM BROWN": "#612E16",
        "LIGHT BROWN": "#8B4B2C",
        "DARK YELLOW": "#858310",
        "MEDIUM YELLOW": "#E2CC20",
        "LIGHT YELLOW": "#E3D372",
        "DARK GREEN": "#232905",
        "MEDIUM GREEN": "#4D4F0D",
        "LIGHT GREEN": "#778811",
    },
    "repolygon_design_4": {
        "DARK RED": "#6C0C02",
        "MEDIUM RED": "#A71A03",
        "ORANGE": "#D95505",
        "SAND": "#EDB279",
        "BLUE": "#3947FF",
    },
    "repolygon_design_5": {
        "BLACK": "#000000",
        "YELLOW": "#EFEF83",
        "DARK BLUE": "#110E20",
        "LIGHT BLUE": "#425182",
        "DARK MAROON": "#1F040A",
        "MEDIUM MAROON": "#3D0B16",
        "LIGHT MAROON": "#771721",
    },
    "repolygon_design_6": {
        "OFF BLACK": "#060606",
        "DARK GREEN": "#176621",
        "MEDIUM GREEN": "#77B06B",
        "LIGHT GREEN": "#B8EFB1",
    },
    "repolygon_design_7": {
        "OFF BLACK": "#071510",
        "KHAKI": "#1E301A",
        "BROWN": "#5C2616",
        "SAND": "#B57F31",
        "YELLOW": "#FBFC80",
    },
    "repolygon_design_8": {
        "OFF BLACK": "#030306",
        "WHITE": "#FFFFFF",
        "GREY": "#332D3F",
        "TEAL": "#002627",
        "BLUE": "#00249A",
        "PURPLE": "#37264B",
        "PINK": "#982B47",
        "RED": "#96231E",
        "BROWN": "#672A1E",
    },
    "repolygon_design_9": {
        "BLACK": "#000000",
        "WHITE": "#FFFFFF",
        "BLUE": "#083C6C",
        "GREEN": "#00765E",
        "DARK TEAL": "#002A3A",
        "MEDIUM TEAL": "#00979C",
        "LIGHT TEAL": "#00BAC6",
    },
    "repolygon_design_10": {
        "BLACK": "#000000",
        "OFF WHITE": "#FAE7B5",
        "YELLOW": "#E3A857",
        "ORANGE": "#AF4035",
        "GREEN": "#1C352D",
    },
    "repolygon_design_11": {
        "OFF BLACK": "#101D18",
        "OFF WHITE": "#F0EAD6",
        "MAROON": "#662628",
        "GREEN": "#144C2E",
    },
}


""" Define data for all minimal-tone example designs in a single dictionary.

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
MINIMAL_TONE_EXAMPLES_SPEC = {
    "repolygon_design_1": (
        [
            ((4, 15.125, 1, (15, 48), (0, 0)), ()),
            ((6, 15.125, 1, (15, 48), (7.5, 24)), ()),
            ((12, 22, 12, (15, 48), (7.5, 24)), ()),
        ],
        ((40, 200, 40, 200),),
    ),
    "repolygon_design_2": (
        [
            ((6, 2, 1, (12.2, 7), (0, 0)), ()),
            ((6, 2, 1, (12.2, 7), (6.1, 3.5)), ()),
            ((12, 6, 1, (12.2, 7), (0, 0)), ()),
            ((12, 6, 1, (12.2, 7), (6.1, 3.5)), ()),
            ((50, 3.5, 6, (12.2, 7), (0, 0)), ()),
            ((50, 3.5, 6, (12.2, 7), (6.1, 3.5)), ()),
        ],
        ((6.1, 42.7, 6.1, 42.7),),
    ),
    "repolygon_design_3": (
        [
            ((4, 1, 1, (6, 6), (2, 2)), (0.75,)),
            ((6, 2, 1, (6, 6), (2, 2)), (0.75,)),
            ((6, 2.75, 1, (6, 6), (5, 5)), (0.75,)),
            ((8, 5, 1, (6, 6), (2, 2)), (0.75,)),
            ((12, 3.5, 1, (6, 6), (2, 2)), (0.75,)),
        ],
        ((2, 26, 2, 26),),
    ),
    "repolygon_design_4": (
        [
            ((16, 0.9, 1, (6, 6), (0, 0)), (1.5,)),
            ((16, 0.9, 1, (6, 6), (3, 3)), (1.5,)),
            ((16, 0.9, 8, (6, 6), (0, 0)), (1.5,)),
            ((16, 0.9, 8, (6, 6), (3, 3)), (1.5,)),
            ((16, 1.8, 1, (6, 6), (0, 0)), (3,)),
            ((16, 1.8, 1, (6, 6), (3, 3)), (3,)),
            ((16, 1.8, 8, (6, 6), (0, 0)), (3,)),
            ((16, 1.8, 8, (6, 6), (3, 3)), (3,)),
            ((16, 2.7, 1, (6, 6), (0, 0)), (4.5,)),
            ((16, 2.7, 1, (6, 6), (3, 3)), (5.5,)),
            ((16, 2.7, 8, (6, 6), (0, 0)), (4.5,)),
            ((16, 2.7, 8, (6, 6), (3, 3)), (4.5,)),
            ((16, 3.6, 1, (6, 6), (0, 0)), (6,)),
            ((16, 3.6, 1, (6, 6), (3, 3)), (6,)),
            ((16, 3.6, 8, (6, 6), (0, 0)), (6,)),
            ((16, 3.6, 8, (6, 6), (3, 3)), (6,)),
        ],
        ((6, 24, 6, 24),),
    ),
    "repolygon_design_5": (
        [
            ((8, 1.6, 8, (4, 4), (0, 0)), (3,)),
            ((8, 2.5, 1, (4, 4), (0, 0)), (2,)),
            ((8, 4, 1, (4, 4), (0, 0)), (2,)),
        ],
        ((0, 20, 0, 20),),
    ),
    "repolygon_design_6": (
        [
            ((4, 1.28, -2.58, (5.6, 5.6), (0, 0)), (2,)),
            ((8, 8.5, 4.25, (5.6, 5.6), (0, 0)), (6,)),
            ((8, 10, 4.25, (5.6, 5.6), (0, 0)), (2,)),
        ],
        ((11.2, 28, 11.2, 28),),
    ),
    "repolygon_design_7": (
        [
            ((12, 0.56, -2.8, (5.6, 5.6), (0, 0)), (7,)),
            ((12, 1.4, -2.8, (5.6, 5.6), (0, 0)), (6,)),
            ((12, 2.24, -2.8, (5.6, 5.6), (0, 0)), (5,)),
            ((12, 3.08, -2.8, (5.6, 5.6), (0, 0)), (4,)),
            ((12, 3.92, -2.8, (5.6, 5.6), (0, 0)), (3,)),
            ((12, 4.72, -2.8, (5.6, 5.6), (0, 0)), (2,)),
            ((12, 5.6, -2.8, (5.6, 5.6), (0, 0)), ()),
        ],
        ((2.8, 19.6, 2.8, 19.6),),
    ),
    "repolygon_design_8": (
        [
            ((4, 0.45, 1, (5.6, 5.6), (0, 2.8)), ()),
            ((4, 0.7, 1, (5.6, 5.6), (0, 2.8)), ()),
            ((6, 0.8, 6, (5.6, 5.6), (2.8, 0)), ()),
            ((6, 1, 6, (5.6, 5.6), (2.8, 0)), ()),
            ((6, 1.8, 6, (5.6, 5.6), (0, 0)), ()),
            ((6, 2, 6, (5.6, 5.6), (0, 0)), ()),
            ((12, 7.8, 12, (5.6, 5.6), (0, 0)), ()),
            ((12, 8, 12, (5.6, 5.6), (0, 0)), ()),
        ],
        ((2.8, 19.6, 2.8, 19.6),),
    ),
    "repolygon_design_9": (
        [
            ((4, 0.7, 4, (8, 8), (2, 2)), ()),
            ((4, 1.1, 4, (8, 8), (2, 2)), ()),
            ((8, 1.7, 1, (4, 4), (0, 0)), ()),
            ((8, 2.0, 1, (4, 4), (0, 0)), ()),
            ((12, 5.7, 12, (8, 8), (2, 2)), ()),
            ((12, 6.0, 12, (8, 8), (2, 2)), ()),
        ],
        ((4, 24, 4, 24),),
    ),
    "repolygon_design_10": (
        [
            (
                (4, 1, 1, (8, 8), (0, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 1),
            ),
            (
                (4, 1, 1, (8, 8), (4, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 2),
            ),
            (
                (4, 2.5, 1, (8, 8), (0, 0)),
                (10, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 9),
            ),
            (
                (4, 2.5, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 5),
            ),
            (
                (4, 2.5, 4, (8, 8), (0, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 10),
            ),
            (
                (4, 2.5, 4, (8, 8), (4, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 6),
            ),
            (
                (4, 3, 1, (8, 8), (0, 0)),
                (10, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 7),
            ),
            (
                (4, 3, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_MID, 3),
            ),
            (
                (4, 3, 4, (8, 8), (0, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_LIGHT, 8),
            ),
            (
                (4, 3, 4, (8, 8), (4, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_MID, 4),
            ),
            (
                (8, 3, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, NO_COLOURING_DARK, 0),
            ),
        ],
        ((4, 36, 4, 36), NO_COLOURING_MID),
    ),
    "repolygon_design_11": (
        [
            (
                (6, 8, 6, (13.86, 24), (0, 0)),
                (
                    2.5,
                    "dashed",
                    NO_COLOURING_DARK,
                    NO_COLOURING_TRANSPARENT,
                    11,
                ),
            ),
            (
                (6, 8, 6, (13.86, 24), (0, 0)),
                (9, "solid", NO_COLOURING_LIGHT, NO_COLOURING_MID, 0),
            ),
            (
                (6, 8, 6, (13.86, 24), (6.93, 12)),
                (
                    2.5,
                    "dashed",
                    NO_COLOURING_DARK,
                    NO_COLOURING_TRANSPARENT,
                    4,
                ),
            ),
            (
                (6, 8, 6, (13.86, 24), (6.93, 12)),
                (9, "solid", NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 1),
            ),
            (
                (50, 1.8, 6, (13.86, 24), (0, 0)),
                (
                    1.5,
                    "solid",
                    NO_COLOURING_LIGHT,
                    NO_COLOURING_TRANSPARENT,
                    10,
                ),
            ),
            (
                (50, 1.8, 6, (13.86, 24), (6.93, 12)),
                (
                    1.5,
                    "solid",
                    NO_COLOURING_LIGHT,
                    NO_COLOURING_TRANSPARENT,
                    7,
                ),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (0, 0)),
                (
                    2.5,
                    "dotted",
                    NO_COLOURING_DARK,
                    NO_COLOURING_TRANSPARENT,
                    8,
                ),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (0, 0)),
                (7, "solid", NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 3),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (6.93, 12)),
                (2.5, "dotted", NO_COLOURING_MID, NO_COLOURING_TRANSPARENT, 5),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (6.93, 12)),
                (7, "solid", NO_COLOURING_LIGHT, NO_COLOURING_TRANSPARENT, 2),
            ),
            (
                (50, 4.4, 6, (13.86, 24), (0, 0)),
                (
                    1.5,
                    "solid",
                    NO_COLOURING_LIGHT,
                    NO_COLOURING_TRANSPARENT,
                    9,
                ),
            ),
            (
                (50, 4.4, 6, (13.86, 24), (6.93, 12)),
                (
                    1.5,
                    "solid",
                    NO_COLOURING_LIGHT,
                    NO_COLOURING_TRANSPARENT,
                    6,
                ),
            ),
        ],
        ((0.0, 55.44, 3.5, 57.94), NO_COLOURING_DARK),
    ),
}


"""
Define data for all true-colour example designs in a single dictionary.

See the docstring on the previous specification dictionary
(MINIMAL_TONE_EXAMPLES_SPEC) for details on the structure and the meaning of
the values within.

"""
FULL_COLOUR_EXAMPLES_SPEC = {
    "repolygon_design_1": (
        [
            (
                (4, 15.125, 1, (15, 48), (0, 0)),
                (1, "solid", "WHITE", NO_COLOURING_TRANSPARENT, -1),
            ),
            (
                (6, 15.125, 1, (15, 48), (7.5, 24)),
                (1, "solid", "WHITE", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 22, 12, (15, 48), (7.5, 24)),
                (1, "solid", "WHITE", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [
            (0, 1, "DARK BROWN", -1),
            (0, 2, "DARK BLUE", -2),
        ],
        ((40, 200, 40, 200), "LIGHT BLUE"),
    ),
    "repolygon_design_2": (
        [
            (
                (6, 2, 1, (12.2, 7), (0, 0)),
                (1, "solid", "SAND", "OFF WHITE", 0),
            ),
            (
                (6, 2, 1, (12.2, 7), (6.1, 3.5)),
                (1, "solid", "SAND", "OFF WHITE", 0),
            ),
            (
                (12, 6, 1, (12.2, 7), (0, 0)),
                (1, "solid", "SAND", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 6, 1, (12.2, 7), (6.1, 3.5)),
                (1, "solid", "SAND", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (50, 3.5, 6, (12.2, 7), (0, 0)),
                (1, "solid", "SAND", "TEAL", -1),
            ),
            (
                (50, 3.5, 6, (12.2, 7), (6.1, 3.5)),
                (1, "solid", "SAND", "TEAL", -1),
            ),
        ],
        [],
        ((6.1, 42.7, 6.1, 42.7), "DARK BROWN"),
    ),
    "repolygon_design_3": (
        [
            (
                (4, 1, 1, (6, 6), (2, 2)),
                (0.75, "solid", "LIGHT PURPLE", "GREY", 0),
            ),
            (
                (6, 2, 1, (6, 6), (2, 2)),
                (0.75, "solid", "LIGHT PURPLE", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (6, 2.75, 1, (6, 6), (5, 5)),
                (0.75, "solid", "LIGHT PURPLE", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (8, 5, 1, (6, 6), (2, 2)),
                (0.75, "solid", "LIGHT PURPLE", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 3.5, 1, (6, 6), (2, 2)),
                (0.75, "solid", "LIGHT PURPLE", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [
            (4, 4, "DARK PURPLE", -1),
        ],
        ((2, 26, 2, 26), "OFF BLACK"),
    ),
    "repolygon_design_4": (
        [
            (
                (16, 0.9, 1, (6, 6), (0, 0)),
                (1.5, "solid", "SAND", "MEDIUM RED", 4),
            ),
            (
                (16, 0.9, 1, (6, 6), (3, 3)),
                (1.5, "solid", "SAND", "MEDIUM RED", 4),
            ),
            ((16, 0.9, 8, (6, 6), (0, 0)), (1.5, "solid", "SAND", "SAND", 3)),
            ((16, 0.9, 8, (6, 6), (3, 3)), (1.5, "solid", "SAND", "SAND", 3)),
            (
                (16, 1.8, 1, (6, 6), (0, 0)),
                (3, "solid", "SAND", "DARK RED", 2),
            ),
            (
                (16, 1.8, 1, (6, 6), (3, 3)),
                (3, "solid", "SAND", "DARK RED", 2),
            ),
            ((16, 1.8, 8, (6, 6), (0, 0)), (3, "solid", "SAND", "BLUE", 1)),
            ((16, 1.8, 8, (6, 6), (3, 3)), (3, "solid", "SAND", "BLUE", 1)),
            (
                (16, 2.7, 1, (6, 6), (0, 0)),
                (4.5, "solid", "SAND", "ORANGE", 0),
            ),
            (
                (16, 2.7, 1, (6, 6), (3, 3)),
                (5.5, "solid", "SAND", "ORANGE", 0),
            ),
            (
                (16, 2.7, 8, (6, 6), (0, 0)),
                (4.5, "solid", "SAND", NO_COLOURING_TRANSPARENT, 8),
            ),
            (
                (16, 2.7, 8, (6, 6), (3, 3)),
                (4.5, "solid", "SAND", NO_COLOURING_TRANSPARENT, 8),
            ),
            (
                (16, 3.6, 1, (6, 6), (0, 0)),
                (6, "solid", "SAND", NO_COLOURING_TRANSPARENT, 9),
            ),
            (
                (16, 3.6, 1, (6, 6), (3, 3)),
                (6, "solid", "SAND", NO_COLOURING_TRANSPARENT, 9),
            ),
            (
                (16, 3.6, 8, (6, 6), (0, 0)),
                (6, "solid", "SAND", NO_COLOURING_TRANSPARENT, 10),
            ),
            (
                (16, 3.6, 8, (6, 6), (3, 3)),
                (6, "solid", "SAND", NO_COLOURING_TRANSPARENT, 10),
            ),
        ],
        [
            (15, 1, "BLUE", -7),
        ],
        ((6, 24, 6, 24), "MEDIUM RED"),
    ),
    "repolygon_design_5": (
        [
            (
                (8, 1.6, 8, (4, 4), (0, 0)),
                (3, "solid", "BLACK", "LIGHT BLUE", 0),
            ),
            (
                (8, 2.5, 1, (4, 4), (0, 0)),
                (2, "solid", "BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (8, 4, 1, (4, 4), (0, 0)),
                (2, "solid", "BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [
            (0, 1, "DARK BLUE", -1),
        ],
        ((0, 20, 0, 20), "LIGHT MAROON"),
    ),
    "repolygon_design_6": (
        [
            (
                (4, 1.28, -2.58, (5.6, 5.6), (0, 0)),
                (2, "solid", "OFF BLACK", "DARK GREEN", -1),
            ),
            (
                (8, 8.5, 4.25, (5.6, 5.6), (0, 0)),
                (6, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (8, 10, 4.25, (5.6, 5.6), (0, 0)),
                (2, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [],
        ((11.2, 28, 11.2, 28), "MEDIUM GREEN"),
    ),
    "repolygon_design_7": (
        [
            (
                (12, 0.56, -2.8, (5.6, 5.6), (0, 0)),
                (7, "solid", "OFF BLACK", "YELLOW", 0),
            ),
            (
                (12, 1.4, -2.8, (5.6, 5.6), (0, 0)),
                (6, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 2.24, -2.8, (5.6, 5.6), (0, 0)),
                (5, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 3.08, -2.8, (5.6, 5.6), (0, 0)),
                (4, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 3.92, -2.8, (5.6, 5.6), (0, 0)),
                (3, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 4.72, -2.8, (5.6, 5.6), (0, 0)),
                (2, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 5.6, -2.8, (5.6, 5.6), (0, 0)),
                (1, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [
            (0, 3, "KHAKI", -1),
        ],
        ((2.8, 19.6, 2.8, 19.6), "SAND"),
    ),
    "repolygon_design_8": (
        [
            (
                (4, 0.45, 1, (5.6, 5.6), (0, 2.8)),
                (1, "solid", "OFF BLACK", "PINK", 1),
            ),
            (
                (4, 0.7, 1, (5.6, 5.6), (0, 2.8)),
                (1, "solid", "OFF BLACK", "WHITE", 0),
            ),
            (
                (6, 0.8, 6, (5.6, 5.6), (2.8, 0)),
                (1, "solid", "OFF BLACK", "RED", 1),
            ),
            (
                (6, 1, 6, (5.6, 5.6), (2.8, 0)),
                (1, "solid", "OFF BLACK", "WHITE", 0),
            ),
            (
                (6, 1.8, 6, (5.6, 5.6), (0, 0)),
                (1, "solid", "OFF BLACK", "BROWN", 1),
            ),
            (
                (6, 2, 6, (5.6, 5.6), (0, 0)),
                (1, "solid", "OFF BLACK", "WHITE", 0),
            ),
            (
                (12, 7.8, 12, (5.6, 5.6), (0, 0)),
                (1, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
            (
                (12, 8, 12, (5.6, 5.6), (0, 0)),
                (1, "solid", "OFF BLACK", NO_COLOURING_TRANSPARENT, 0),
            ),
        ],
        [],
        ((2.8, 19.6, 2.8, 19.6), "TEAL"),
    ),
    "repolygon_design_9": (
        [
            (
                (4, 0.7, 4, (8, 8), (2, 2)),
                (1, "solid", "BLACK", "MEDIUM TEAL", 2),
            ),
            ((4, 1.1, 4, (8, 8), (2, 2)), (1, "solid", "BLACK", "WHITE", 1)),
            ((8, 1.7, 1, (4, 4), (0, 0)), (1, "solid", "BLACK", "BLUE", 4)),
            ((8, 2.0, 1, (4, 4), (0, 0)), (1, "solid", "BLACK", "WHITE", 3)),
            (
                (12, 5.7, 12, (8, 8), (2, 2)),
                (1, "solid", "BLACK", NO_COLOURING_TRANSPARENT, 6),
            ),
            (
                (12, 6.0, 12, (8, 8), (2, 2)),
                (1, "solid", "BLACK", NO_COLOURING_TRANSPARENT, 6),
            ),
        ],
        [],
        ((4, 24, 4, 24), "LIGHT TEAL"),
    ),
    "repolygon_design_10": (  # done!
        [
            (
                (4, 1, 1, (8, 8), (0, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "BLACK", 1),
            ),
            (
                (4, 1, 1, (8, 8), (4, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "BLACK", 2),
            ),
            (
                (4, 2.5, 1, (8, 8), (0, 0)),
                (10, "solid", NO_COLOURING_TRANSPARENT, "GREEN", 9),
            ),
            (
                (4, 2.5, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, "OFF WHITE", 5),
            ),
            (
                (4, 2.5, 4, (8, 8), (0, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "GREEN", 10),
            ),
            (
                (4, 2.5, 4, (8, 8), (4, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "OFF WHITE", 6),
            ),
            (
                (4, 3, 1, (8, 8), (0, 0)),
                (10, "solid", NO_COLOURING_TRANSPARENT, "OFF WHITE", 7),
            ),
            (
                (4, 3, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, "BLACK", 3),
            ),
            (
                (4, 3, 4, (8, 8), (0, 0)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "OFF WHITE", 8),
            ),
            (
                (4, 3, 4, (8, 8), (4, 4)),
                (3, "solid", NO_COLOURING_TRANSPARENT, "BLACK", 4),
            ),
            (
                (8, 3, 1, (8, 8), (4, 4)),
                (10, "solid", NO_COLOURING_TRANSPARENT, "ORANGE", 0),
            ),
        ],
        [],
        ((4, 36, 4, 36), "YELLOW"),
    ),
    "repolygon_design_11": (  # done!
        [
            (
                (6, 8, 6, (13.86, 24), (0, 0)),
                (2.5, "dashed", "OFF BLACK", NO_COLOURING_TRANSPARENT, 11),
            ),
            (
                (6, 8, 6, (13.86, 24), (0, 0)),
                (9, "solid", "OFF WHITE", "GREEN", 0),
            ),
            (
                (6, 8, 6, (13.86, 24), (6.93, 12)),
                (2.5, "dashed", "OFF BLACK", NO_COLOURING_TRANSPARENT, 4),
            ),
            (
                (6, 8, 6, (13.86, 24), (6.93, 12)),
                (9, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 1),
            ),
            (
                (50, 1.8, 6, (13.86, 24), (0, 0)),
                (1.5, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 10),
            ),
            (
                (50, 1.8, 6, (13.86, 24), (6.93, 12)),
                (1.5, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 7),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (0, 0)),
                (2.5, "dotted", "MAROON", NO_COLOURING_TRANSPARENT, 8),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (0, 0)),
                (7, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 3),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (6.93, 12)),
                (2.5, "dotted", "GREEN", NO_COLOURING_TRANSPARENT, 5),
            ),
            (
                (50, 3.1, 6, (13.86, 24), (6.93, 12)),
                (7, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 2),
            ),
            (
                (50, 4.4, 6, (13.86, 24), (0, 0)),
                (1.5, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 9),
            ),
            (
                (50, 4.4, 6, (13.86, 24), (6.93, 12)),
                (1.5, "solid", "OFF WHITE", NO_COLOURING_TRANSPARENT, 6),
            ),
        ],
        [],
        ((0.0, 55.44, 3.5, 57.94), "MAROON"),
    ),
}


"""Define data to recreate the iconic carpet from Kubrick's film 'The Shining'.

Specifically, provide the design and colours to replicate, and to render a
variation that has different colours and highlights the underlying pattern of,
the famous hexagonal-based patterned carpet from the Overlook Hotel setting
in the film 'The Shining', directed and produced by Stanley Kubrick.

See the above docstrings for documentation that describes the meaning of
the structure and of any values supplied.

"""
CARPET_KUBRICK_THE_SHINING_COLOURS = {
    # Actual carpet colours picked out from still of film:
    "ACTUAL_DESIGN": {
        "ORANGE": "#B0522E",
        "BROWN": "#40221A",
        "MAROON": "#772120",
    },
    # Alternatve (much nicer!) colours for an original variant on the design:
    "ALTERNATIVE_COLOUR_DESIGN": {
        "DARK NAVY": "#0C0A3E",
        "BRIGHT MINT GREEN": "#ADF1D2",
        "DARK MINT GREEN": "#669982",
        "BRIGHT CERISE": "#D74264",
        "DARK CERISE": "#7E1B32",
    },
}
CARPET_KUBRICK_THE_SHINING_SPEC = {
    "ACTUAL_DESIGN": (
        [
            # For the hexagonal underlying grid:
            (
                (6, 16, 6, (27.72, 40), (0, 16)),
                (6.5, "solid", "BROWN", NO_COLOURING_TRANSPARENT, 1, 20, 2),
            ),
            (
                (6, 16, 1.2, (27.72, 40), (13.86, 0)),
                (6.5, "solid", "BROWN", NO_COLOURING_TRANSPARENT, 0, 20, 2),
            ),
            # For the smaller hexagons inside the hexagonal grid:
            (
                (6, 7, 6, (27.72, 40), (13.86, 0 + 0.4)),
                (6.5, "solid", "BROWN", "MAROON", 20),
            ),
            (
                (6, 7, 6, (27.72, 40), (0, 16 - 0.4)),
                (6.5, "solid", "BROWN", "MAROON", 21),
            ),
        ],
        ((40, 200, 40, 200), "ORANGE"),
    ),
    "ALTERNATIVE_COLOUR_DESIGN": (
        [
            # For the hexagonal underlying grid:
            (
                (6, 16, 6, (27.72, 40), (0, 16)),
                (
                    6.5,
                    "solid",
                    "BRIGHT MINT GREEN",
                    NO_COLOURING_TRANSPARENT,
                    1,
                    20,
                    2,
                ),
            ),
            (
                (6, 16, 1.2, (27.72, 40), (13.86, 0)),
                (
                    6.5,
                    "solid",
                    "DARK MINT GREEN",
                    NO_COLOURING_TRANSPARENT,
                    0,
                    20,
                    2,
                ),
            ),
            # For the smaller hexagons inside the hexagonal grid:
            (
                (6, 7, 6, (27.72, 40), (13.86, 0 + 0.4)),
                (6.5, "solid", "BRIGHT MINT GREEN", "BRIGHT CERISE", 20),
            ),
            (
                (6, 7, 6, (27.72, 40), (0, 16 - 0.4)),
                (6.5, "solid", "DARK MINT GREEN", "DARK CERISE", 21),
            ),
        ],
        ((40, 200, 40, 200), "DARK NAVY"),
    ),
}
