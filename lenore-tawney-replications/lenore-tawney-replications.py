"""Replication of, and variations on, linear drawings by Lenore Tawney.

All six original drawings that are replicated were completed in 1964.

See also Tawney's website for information about the artist of the original
works:
  https://lenoretawney.org/

"""

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.patches import Polygon
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator


# See comments against first item for documentation of these design parameters
REPLICATION_DESIGN_PARAMETERS = {
    "The Great Breath": (
        # Coordinates of start and end points of all lines to draw.
        [
            ((9, 81), (80, 92)),
            ((80, 92), (150, 81)),
            ((10, 15), (80, 6)),
            ((80, 6), (150, 15)),
            ((10, 40), (80, 6)),
            ((80, 6), (150, 40)),
        ],
        # All pairs of lines, identified by (zero-indexed) position in above
        # line coordinates listing, to be joined together with many lines from
        # points equally-spaced and sequentially drawn across both lines.
        [(0, 3), (1, 2), (1, 4), (0, 5)],
        # Design style, three-tuple of:
        #   1. figsize, scaling_factor;
        #   2. of lines: line width, line alpha, wiggliness (via rcparams);
        #   3. colours: background colour, grid colour, line colour.
        #   4. (optional) change to the number of lines to draw between coors
        (
            ((11, 6.75), 100),
            (0.4, 0.6, False),
            ("#E7DACB", "#9EC3EA", "#2F1E1E"),
        ),
        # Optional dict to override colour for given coor pair (by index).
        {},
        # Optional list to plot a regular polygon, as required for some designs
        # where the 6-tuple gives:
        # (number of sides, centre position, radius, rotational factor, colour,
        # optional Bool for whether or not to plot lines across assumed False)
        [],
    ),
    "Wings of the Wind": (
        [
            ((25, 50), (105, 25)),
            ((105, 25), (185, 50)),
            ((25, 129), (105, 121)),
            ((105, 121), (185, 129)),
        ],
        [(0, 3), (1, 2)],
        (
            ((8, 6), 160),
            (0.35, 0.7, False),
            ("#E6DFD5", "#BCB9A9", "#37272A"),
        ),
    ),
    "From Its Center": (
        [
            ((5, 15), (65, 15)),
            ((5, 75), (35, 95)),
            ((35, 95), (65, 75)),
        ],
        [
            (0, 1),
            (0, 2),
        ],
        (
            ((4, 5.75), 70),  # 10 up by 7 across
            (0.5, 1.0, False),
            ("#F7F3F0", "#1C1815", "#030000"),
        ),
    ),
    "Union of Water and Fire II": (
        [
            ((20, 130), (140, 130)),
            ((20, 70), (140, 70)),
        ],
        [((80, 40), 0), ((80, 160), 1)],
        (
            ((5, 6.25), 160),  # 20 by 16 (TODO: thicker half grid lines too)
            (0.5, 0.4, False),
            ("#E8E3DD", "#E0A66C", "#464476"),
            100,
        ),
        {1: "#E75136"},
    ),
    "The Eternal Band": (
        [
            ((60, 60), (60.26126851, 99.99914673)),
            ((60, 60), (28.89030607, 85.14332801)),
            ((60, 60), (20.94557768, 51.35407047)),
            ((60, 60), (42.40962587, 24.07537421)),
            ((60, 60), (77.11958455, 23.8486539)),
            ((60, 60), (98.93814689, 50.84463455)),
            ((60, 60), (91.43549043, 84.73479212)),
        ],
        [
            # 6, 0 -> 5 and not 1 -> 6, 0 to give join lines pointing clockwise
            ((60.26126851, 99.99914673), 6),
            ((28.89030607, 85.14332801), 0),
            ((20.94557768, 51.35407047), 1),
            ((42.40962587, 24.07537421), 2),
            ((77.11958455, 23.8486539), 3),
            ((98.93814689, 50.84463455), 4),
            ((91.43549043, 84.73479212), 5),
        ],
        (
            ((8, 8), 120),  # 20 by 16 (TODO: thicker half grid lines too)
            (0.5, 0.7, False),
            # Fake having no gridlines by plotting in background colour!
            ("#ECEDEF", "#ECEDEF", "#C8431E"),
            30,
        ),
        {},
        # First polygon approximates a circle with high enough N of sides
        [
            (1000, (60, 60), 40, 1, "#C8431E"),
            # Use Pythagoras' theorem to have square sides tangential to circle
            (4, (60, 60), np.sqrt(2 * 40 ** 2), 4, "#827876"),
            # Don't plot this, but the following was uncommented and printed
            # out later in the code to get the points for the design:
            # (7, (60, 60), 40, 1.5 * np.pi, "#1B1818"),  # to print for points
        ],
    ),
    "Blue Circle": (
        [
            ((195, 80), (585, 80)),
            ((195, 470), (585, 470)),
            ((195, 80), (195, 470)),
            ((585, 80), (585, 470)),
        ],
        [(0, 1), (2, 3)],
        (
            ((8.5, 6), 550),
            (0.5, 0.6, False),
            ("#E1D9CC", "#B4AD9D", "#2D2306"),
            120,
        ),
        {},
        [
            # Approximates a circle with high enough N of sides but here the
            # N approximation is also the number of lines used to join circle
            (4 * 120, (390, 275), 70, 1, "#2541C1", True),
        ],
    ),
}


VARIATION_DESIGN_PARAMETERS = {
    "Treble Clef": (
        [
            ((0, 30), (60, 80)),
            ((50, 0), (100, 0)),
            ((30, 70), (100, 20)),
            ((0, 0), (50, 0)),
            ((100, 70), (40, 20)),
            ((50, 100), (0, 100)),
            ((70, 30), (0, 80)),
            ((100, 100), (50, 100)),
            ((40, 20), (50, 0)),
            ((50, 100), (60, 80)),
        ],
        [
            (0, 3),
            (1, 2),
            (4, 7),
            (5, 6),
            (8, 9),
        ],
        (
            ((8, 8), 100),
            (1.0, 0.7, False),
            ("#D7DEE4", "#7C86B9", "#0C2027"),
        ),
    ),
    "Softening": (
        [
            # Lines of the *outermost* octagon:
            ((15, 5), (35, 5)),
            ((35, 45), (15, 45)),
            ((5, 15), (5, 35)),
            ((45, 35), (45, 15)),
            ((15, 45), (5, 35)),
            ((35, 45), (45, 35)),
            ((15, 5), (5, 15)),
            ((35, 5), (45, 15)),
            # Lines of the octagon next-in from the outermost:
            ((10, 30), (10, 20)),
            ((10, 30), (20, 40)),
            ((20, 40), (30, 40)),
            ((40, 30), (30, 40)),
            ((40, 20), (40, 30)),
            ((40, 20), (30, 10)),
            ((30, 10), (20, 10)),
            ((10, 20), (20, 10)),
            # Lines of the octagon twice-in from the outermost, and next-out
            # from the innermost.
            # Note: created by changing from above eight 10 -> 15, 40 -> 35.
            ((15, 30), (15, 20)),
            ((15, 30), (20, 35)),
            ((20, 35), (30, 35)),
            ((35, 30), (30, 35)),
            ((35, 20), (35, 30)),
            ((35, 20), (30, 15)),
            ((30, 15), (20, 15)),
            ((15, 20), (20, 15)),
            # Lines of the *innermost* octagon.
            # Note: similar (and further) transformations made as with above.
            ((17.5, 27.5), (17.5, 22.5)),
            ((17.5, 27.5), (22.5, 32.5)),
            ((22.5, 32.5), (27.5, 32.5)),
            ((32.5, 27.5), (27.5, 32.5)),
            ((32.5, 22.5), (32.5, 27.5)),
            ((32.5, 22.5), (27.5, 17.5)),
            ((27.5, 17.5), (22.5, 17.5)),
            ((17.5, 22.5), (22.5, 17.5)),
        ],
        [
            # Inter-connections between the lines of the *outermost* octagon:
            (0, 3),
            (1, 2),
            (0, 2),
            (1, 3),
            (4, 5),
            (6, 7),
            (4, 6),
            (5, 7),
            # Inter-connections between the lines of the octagon next-in from
            # the outermost:
            (8, 10),
            (8, 14),
            (10, 12),
            (12, 14),
            (9, 11),
            (11, 13),
            (13, 15),
            (9, 15),
            # Inter-connections between the lines of the octagon twice-in from
            # the outermost, and next-out from the innermost:
            (16, 18),
            (16, 22),
            (18, 20),
            (20, 22),
            (17, 19),
            (19, 21),
            (21, 23),
            (17, 23),
            # Inter-connections between the lines of the *innermost* octagon:
            (24, 26),
            (24, 30),
            (26, 28),
            (28, 30),
            (25, 27),
            (27, 29),
            (29, 31),
            (25, 31),
        ],
        (
            ((8, 8), 50),
            (0.6, 0.6, False),
            ("#FBF4EA", "powderblue", "#180202"),
            50,
        ),
    ),
    "Crosses on our Eyes": (
        [
            ((60, 20), (60, 80)),
            ((0, 0), (20, 80)),
            ((100, 100), (20, 80)),
            ((80, 40), (20, 40)),
            ((40, 80), (40, 20)),
            ((100, 100), (80, 20)),
            ((0, 0), (80, 20)),
            ((20, 60), (80, 60)),
            ((40, 20), (60, 20)),
            ((40, 80), (60, 80)),
            ((20, 40), (20, 60)),
            ((80, 40), (80, 60)),
        ],
        [
            (0, 1),
            (2, 3),
            (4, 5),
            (6, 7),
            (0, 7),
            (3, 4),
            (1, 6),
            (2, 5),
        ],
        (
            ((6, 6), 100),
            (0.3, 0.5, False),
            ("#F3FAF1", "#7BCBEE", "#313036"),
            70,
        ),
        {},
        [
            (1000, (50, 50), 6, 1, "#313036", True),
        ],
    ),
    "Owl": (
        [
            ((10, 0), (10, 50)),
            ((10, 65), (10, 80)),
            ((70, 0), (70, 60)),
            ((70, 65), (70, 80)),
            ((10, 0.1), (27.5, 0.1)),
            ((70, 0.1), (35, 0.1)),
            ((30, 80), (10, 80)),
            ((50, 80), (70, 80)),
            ((35, 5), (35, 50)),
            ((35, 50), (35, 70)),
            ((17.5, 50), (35, 50)),
            ((35, 50), (55, 50)),
            ((35, 77.5), (35, 50)),
            ((35, 50), (35, 25)),
            ((22.5, 50), (35, 50)),
            ((35, 50), (45, 50)),
        ],
        [
            (0, 4),
            (1, 6),
            (2, 5),
            (3, 7),
            (8, 10),
            (9, 11),
            (12, 14),
            (13, 15),
        ],
        (
            ((6, 6), 80),
            (0.5, 1.0, False),
            ("#e6e6cb", "#428a42", "#030000"),
            60,
        ),
        {},
        [
            (100, (55, 65), 6, 1, "#030000", True),
            (63, (22.5, 65), 5, 1, "#030000", True),
        ],
    ),
    "Jaws of Resonance": (
        [
            ((10, 37.5), (45, 2.5)),
            ((20, 37.5), (45, 12.5)),
            ((30, 37.5), (45, 22.5)),
            ((40, 37.5), (45, 32.5)),
            ((50, 37.5), (45, 32.5)),
            ((60, 37.5), (45, 22.5)),
            ((70, 37.5), (45, 12.5)),
            ((80, 37.5), (45, 2.5)),
            ((20, 47.5), (10, 37.5)),
            ((30, 47.5), (20, 37.5)),
            ((40, 47.5), (30, 37.5)),
            ((50, 47.5), (40, 37.5)),
            ((60, 47.5), (50, 37.5)),
            ((70, 47.5), (60, 37.5)),
            ((20, 47.5), (30, 37.5)),
            ((30, 47.5), (40, 37.5)),
            ((40, 47.5), (50, 37.5)),
            ((50, 47.5), (60, 37.5)),
            ((60, 47.5), (70, 37.5)),
            ((70, 47.5), (80, 37.5)),
            ((25, 47.5), (35, 57.5)),
            ((35, 47.5), (45, 57.5)),
            ((45, 47.5), (55, 57.5)),
            ((55, 47.5), (65, 57.5)),
            ((65, 47.5), (75, 57.5)),
            ((25, 47.5), (15, 57.5)),
            ((35, 47.5), (25, 57.5)),
            ((45, 47.5), (35, 57.5)),
            ((55, 47.5), (45, 57.5)),
            ((65, 47.5), (55, 57.5)),
            ((15, 57.5), (45, 87.5)),
            ((25, 57.5), (45, 77.5)),
            ((35, 57.5), (45, 67.5)),
            ((55, 57.5), (45, 67.5)),
            ((65, 57.5), (45, 77.5)),
            ((75, 57.5), (45, 87.5)),
        ],
        [
            (0, 7), (1, 6), (2, 5), (3, 4),
            (30, 35), (31, 34), (32, 33),
            (8, 14), (9, 15), (10, 16), (11, 17), (12, 18), (13, 19),
            (20, 25), (21, 26), (22, 27), (23, 28), (24, 29),  
        ],
        (
            ((6, 6), 90),
            (0.8, 0.4, False),
            ("#03301a", "#28a4a4", "#cff1fc"),
            26,
        ),
    ),
    "Always the Hourglass": (
        [
            # Core central z level
            # Diagonal line
            ((20, 20), (40, 40)),  # no 0
            ((40, 40), (60, 60)),
            ((60, 60), (80, 80)),
            ((80, 80), (100, 100)),
            ((100, 100), (120, 120)),
            ((120, 120), (140, 140)),
            ((140, 140), (160, 160)),
            ((160, 160), (180, 180)),
            ((180, 180), (200, 200)),
            ((200, 200), (220, 220)),
            ((220, 220), (240, 240)),
            ((240, 240), (260, 260)),
            ((260, 260), (280, 280)),
            ((280, 280), (300, 300)),
            ((300, 300), (320, 320)),
            ((320, 320), (340, 340)),
            ((340, 340), (360, 360)),
            ((360, 360), (380, 380)),
            ((380, 380), (400, 400)),
            ((400, 400), (420, 420)),
            ((420, 420), (440, 440)),
            ((440, 440), (460, 460)),
            ((460, 460), (480, 480)),
            ((480, 480), (500, 500)),
            ((500, 500), (520, 520)), # np 25 - 1 = 24 (25 in total)
            # Horizontal line at top
            ((20, 20), (40, 20)), # no 25
            ((40, 20), (60, 20)),
            ((60, 20), (80, 20)),
            ((80, 20), (100, 20)),
            ((100, 20), (120, 20)),
            ((120, 20), (140, 20)),
            ((140, 20), (160, 20)),
            ((160, 20), (180, 20)),
            ((180, 20), (200, 20)),
            ((200, 20), (220, 20)),
            ((220, 20), (240, 20)),
            ((240, 20), (260, 20)),
            ((260, 20), (280, 20)),
            ((280, 20), (300, 20)),
            ((300, 20), (320, 20)),
            ((320, 20), (340, 20)),
            ((340, 20), (360, 20)),
            ((360, 20), (380, 20)),
            ((380, 20), (400, 20)),
            ((400, 20), (420, 20)),
            ((420, 20), (440, 20)),
            ((440, 20), (460, 20)),
            ((460, 20), (480, 20)),
            ((480, 20), (500, 20)),
            ((500, 20), (520, 20)),  # no 50 - 1 = 49
            # Horizontal line at bottom
            ((20, 520), (40, 520)),  # no 50
            ((40, 520), (60, 520)),
            ((60, 520), (80, 520)),
            ((80, 520), (100, 520)),
            ((100, 520), (120, 520)),
            ((120, 520), (140, 520)),
            ((140, 520), (160, 520)),
            ((160, 520), (180, 520)),
            ((180, 520), (200, 520)),
            ((200, 520), (220, 520)),
            ((220, 520), (240, 520)),
            ((240, 520), (260, 520)),
            ((260, 520), (280, 520)),
            ((280, 520), (300, 520)),
            ((300, 520), (320, 520)),
            ((320, 520), (340, 520)),
            ((340, 520), (360, 520)),
            ((360, 520), (380, 520)),
            ((380, 520), (400, 520)),
            ((400, 520), (420, 520)),
            ((420, 520), (440, 520)),
            ((440, 520), (460, 520)),
            ((460, 520), (480, 520)),
            ((480, 520), (500, 520)),
            ((500, 520), (520, 520)),  # no 75 - 1 = 74
            # Next z level - reverse z shape, same but for reflection
            ((20, 520), (40, 500)),  # no 75
            ((40, 500), (60, 480)),
            ((60, 480), (80, 460)),
            ((80, 460), (100, 440)),
            ((100, 440), (120, 420)),
            ((120, 420), (140, 400)),
            ((140, 400), (160, 380)),
            ((160, 380), (180, 360)),
            ((180, 360), (200, 340)),
            ((200, 340), (220, 320)),
            ((220, 320), (240, 300)),
            ((240, 300), (260, 280)),
            ((260, 280), (280, 260)),
            ((280, 260), (300, 240)),
            ((300, 240), (320, 220)),
            ((320, 220), (340, 200)),
            ((340, 200), (360, 180)),
            ((360, 180), (380, 160)),
            ((380, 160), (400, 140)),
            ((400, 140), (420, 120)),
            ((420, 120), (440, 100)),
            ((440, 100), (460, 80)),
            ((460, 80), (480, 60)),
            ((480, 60), (500, 40)),
            ((500, 40), (520, 20)), # 100 - 1 = 99 (100 in total)
            # Vertical line at left
            ((20, 20), (20, 40)), # no 100
            ((20, 40), (20, 60)),
            ((20, 60), (20, 80)),
            ((20, 80), (20, 100)),
            ((20, 100), (20, 120)),
            ((20, 120), (20, 140)),
            ((20, 140), (20, 160)),
            ((20, 160), (20, 180)),
            ((20, 180), (20, 200)),
            ((20, 200), (20, 220)),
            ((20, 220), (20, 240)),
            ((20, 240), (20, 260)),
            ((20, 260), (20, 280)),
            ((20, 280), (20, 300)),
            ((20, 300), (20, 320)),
            ((20, 320), (20, 340)),
            ((20, 340), (20, 360)),
            ((20, 360), (20, 380)),
            ((20, 380), (20, 400)),
            ((20, 400), (20, 420)),
            ((20, 420), (20, 440)),
            ((20, 440), (20, 460)),
            ((20, 460), (20, 480)),
            ((20, 480), (20, 500)),
            ((20, 500), (20, 520)),  # no 125 - 1 = 124
            # Vertical line at right
            ((520, 20), (520, 40)), # no 125
            ((520, 40), (520, 60)),
            ((520, 60), (520, 80)),
            ((520, 80), (520, 100)),
            ((520, 100), (520, 120)),
            ((520, 120), (520, 140)),
            ((520, 140), (520, 160)),
            ((520, 160), (520, 180)),
            ((520, 180), (520, 200)),
            ((520, 200), (520, 220)),
            ((520, 220), (520, 240)),
            ((520, 240), (520, 260)),
            ((520, 260), (520, 280)),
            ((520, 280), (520, 300)),
            ((520, 300), (520, 320)),
            ((520, 320), (520, 340)),
            ((520, 340), (520, 360)),
            ((520, 360), (520, 380)),
            ((520, 380), (520, 400)),
            ((520, 400), (520, 420)),
            ((520, 420), (520, 440)),
            ((520, 440), (520, 460)),
            ((520, 460), (520, 480)),
            ((520, 480), (520, 500)),
            ((520, 500), (520, 520)),  # no 150 - 1 = 149
        ],
        [
            # First vertical connections
            (0, 25),
            (2, 27),
            (4, 29),
            (6, 31),
            (8, 33),
            (10, 35),
            (12, 37),
            (14, 39),
            (16, 41),
            (18, 43),
            (20, 45),
            (22, 47),
            (24, 49),
            # next level
            (1, 51),
            (3, 53),
            (5, 55),
            (7, 57),
            (9, 59),
            (11, 61),
            (13, 63),
            (15, 65),
            (17, 67),
            (19, 69),
            (21, 71),
            (23, 73),
            # Same but for reflection
            (75, 25),
            (77, 27),
            (79, 29),
            (81, 31),
            (83, 33),
            (85, 35),
            (87, 37),
            (89, 39),
            (91, 41),
            (93, 43),
            (95, 45),
            (97, 47),
            (99, 49),
            # next level
            (76, 51),
            (78, 53),
            (80, 55),
            (82, 57),
            (84, 59),
            (86, 61),
            (88, 63),
            (90, 65),
            (92, 67),
            (94, 69),
            (96, 71),
            (98, 73),
        ],
        (
            # ((8.5, 8.5), 540),
            # (0.5, 0.7, False),
            # ("#faffff", "#6bc7c7", "#333333", True),
            # 18,
            ((8.5, 8.5), 540),
            (0.40, 0.65, False),
            ("#faffff", "#6bc7c7", "#333333", True),
            12,
        ),
        {},
        [
        ],
    ),
    "Angry Eyes and Mouth of a God": (
        [
            # Note pattern in general for each triangle 'tri') coords
            # (a, b)
            # (a, c)
            # (b, c)
            # and note that '180 - ' is to flip horizontally from original
            # exploratory work to create 'face' like design
            #
            # Smallest/core (1 x size) tris
            ((0, 180 - 12), (60, 180 - 12)),
            ((0, 180 - 12), (30, 180 - (12 + 10*np.sqrt(27)))),
            ((60, 180 - 12), (30, 180 - (12 + 10*np.sqrt(27)))), # no2
            ((60, 180 - 12), (90, 180 - (12 + 10*np.sqrt(27)))),
            ((30, 180 - (12 + 10*np.sqrt(27))), (90, 180 - (12 + 10*np.sqrt(27)))), # no4
            ((60, 180 - 12), (120, 180 - 12)),
            ((120, 180 - 12), (90, 180 - (12 + 10*np.sqrt(27)))), # no6
            ((120, 180 - 12), (150, 180 - (12 + 10*np.sqrt(27)))),
            ((90, 180 - (12 + 10*np.sqrt(27))), (150, 180 - (12 + 10*np.sqrt(27)))), # no8
            ((120, 180 - 12), (180, 180 - 12)),
            ((180, 180 - 12), (150, 180 - (12 + 10*np.sqrt(27)))), # no10
            ((30, 180 - (12 + 10*np.sqrt(27))), (60, 180 - (12 + 20*np.sqrt(27)))),
            ((90, 180 - (12 + 10*np.sqrt(27))), (60, 180 - (12 + 20*np.sqrt(27)))), # no12
            ((90, 180 - (12 + 10*np.sqrt(27))), (120, 180 - (12 + 20*np.sqrt(27)))),
            ((60, 180 - (12 + 20*np.sqrt(27))), (120, 180 - (12 + 20*np.sqrt(27)))), # no14
            ((90, 180 - (12 + 10*np.sqrt(27))), (150, 180 - (12 + 10*np.sqrt(27)))),
            ((150, 180 - (12 + 10*np.sqrt(27))), (120, 180 - (12 + 20*np.sqrt(27)))), # no16
            ((60, 180 - (12 + 20*np.sqrt(27))), (90, 180 - (12 + 30*np.sqrt(27)))),
            ((120, 180 - (12 + 20*np.sqrt(27))), (90, 180 - (12 + 30*np.sqrt(27)))), # no18
            #
            # Bigger (2 and 3 x) size tris
            # 2 x size tri 0
            ((0, 180 - 12), (120, 180 - 12)),  # no19
            ((0, 180 - 12), (60, 180 - (12 + 20*np.sqrt(27)))),
            ((120, 180 - 12), (60, 180 - (12 + 20*np.sqrt(27)))),  # no21
            # 2 x size tri 1
            ((60, 180 - 12), (180, 180 - 12)),
            ((60, 180 - 12), (120, 180 - (12 + 20*np.sqrt(27)))),
            ((180, 180 - 12), (120, 180 - (12 + 20*np.sqrt(27)))),  # no24
            # 2 x size tri 2
            ((30, 180 - (12 + 10*np.sqrt(27))), (150, 180 - (12 + 10*np.sqrt(27)))),
            ((30, 180 - (12 + 10*np.sqrt(27))), (90, 180 - (12 + 30*np.sqrt(27)))),
            ((150, 180 - (12 + 10*np.sqrt(27))), (90, 180 - (12 + 30*np.sqrt(27)))),  #no27
            # 3 x size (max, outline) tri 0
            ((0, 180 - 12), (180, 180 - 12)),
            ((0, 180 - 12), (90, 180 - (12 + 30*np.sqrt(27)))),
            ((180, 180 - 12), (90, 180 - (12 + 30*np.sqrt(27)))),  #no30
        ],
        [
            # Same size tris:
            (0, 1),
            (17, 18),
            (-9, 10),
            # Corners of 2 x size tris:
            # Bottom left corner
            (0, 20),
            (0, 29),
            (1, 19),
            (1, 28),
            # Bottom right corner
            (17, 30),
            (17, 27),
            (18, 29),
            (18, 26),
            # Top corner
            (-9, 24),
            (-9, 30),
            (-10, 28),
            (-10, 22),
            # Spike in middle - use 2 x triangles but not on corners:
            (20, 21),
            (-19, 21),
            (22, 23),
            (24, 23),
            (26, 25),
            (-27, 25),
            (12, 13),
            (3, 4),
            (-6, 8),
        ],
        (
            ((12, 12), 180),
            (0.3, 0.4, False),
            ("#fffcfc", "#ff8080", "#3b443f", True),
            201,
        ),
    ),
    "Primitive Surveillance": (
        [
            # Zig-zag pattern across column 14
            ((10, 10), (40, 40)),
            ((40, 40), (10, 70)),
            ((10, 70), (40, 100)),
            ((40, 100), (10, 130)),
            ((10, 130), (40, 160)),
            ((40, 160), (10, 190)),
            # Next column - with switch to reflect in y axis
            ((70, 10), (40, 40)),
            ((40, 40), (70, 70)),
            ((70, 70), (40, 100)),
            ((40, 100), (70, 130)),
            ((70, 130), (40, 160)),
            ((40, 160), (70, 190)),
            # Next - follow same pattern to increment values of tuples
            ((70, 10), (100, 40)),
            ((100, 40), (70, 70)),
            ((70, 70), (100, 100)),
            ((100, 100), (70, 130)),
            ((70, 130), (100, 160)),
            ((100, 160), (70, 190)),
            # and more... - with switch to reflect in y axis
            ((130, 10), (100, 40)),
            ((100, 40), (130, 70)),
            ((130, 70), (100, 100)),
            ((100, 100), (130, 130)),
            ((130, 130), (100, 160)),
            ((100, 160), (130, 190)),
            # and more
            ((130, 10), (160, 40)),
            ((160, 40), (130, 70)),
            ((130, 70), (160, 100)),
            ((160, 100), (130, 130)),
            ((130, 130), (160, 160)),
            ((160, 160), (130, 190)),
            # and final one - with switch to reflect in y axis
            ((190, 10), (160, 40)),
            ((160, 40), (190, 70)),
            ((190, 70), (160, 100)),
            ((160, 100), (190, 130)),
            ((190, 130), (160, 160)),
            ((160, 160), (190, 190)),
        ],
        [
            # Winerack-esque outline start
            # Set 0
            (5, 11),
            (17, 23),
            (29, 35),
            (11, 17),
            (23, 29),
            # Set 1
            (4, 10),
            (16, 22),
            (28, 34),
            (10, 16),
            (22, 28),
            # Set 2
            (3, 9),
            (15, 21),
            (27, 33),
            (9, 15),
            (21, 27),
            # Set 3
            (2, 8),
            (14, 20),
            (26, 32),
            (8, 14),
            (20, 26),
            # Set 4
            (1, 7),
            (13, 19),
            (25, 31),
            (7, 13),
            (19, 25),
            # Set 5
            (0, 6),
            (12, 18),
            (24, 30),
            (6, 12),
            (18, 24),
            # Wine rack outline end
            # Sides joining up
            (0, -1),
            (-2, 3),
            (-4, 5),
            (-30, 31),
            (-32, 33),
            (-34, 35),
        ],
        (
            ((6, 6), 200),
            (0.45, 0.7, False),
            ("#eee3dc", "#c1803e", "#240f00"),
            39,
        ),
        {},
        [
            (66, (70 - 2, 40 - 10), 4, 1, "#240f00", True),
            (66, (130 + 2, 40 - 5), 6, 1, "#240f00", True),
            (66, (40 - 4, 70), 10, 1, "#240f00", True),
            (66, (100 + 3, 70 + 5), 7, 1, "#240f00", True),
            (66, (160 - 2, 70 + 10), 3, 1, "#240f00", True),
            (66, (70 + 4, 100 - 10), 4, 1, "#240f00", True),
            (66, (130 - 3, 100 - 5), 6, 1, "#240f00", True),
            (66, (40 + 5, 130), 10, 1, "#240f00", True),
            (66, (100 - 4, 130 + 5), 7, 1, "#240f00", True),
            (66, (160 + 2, 130 + 10), 3, 1, "#240f00", True),
            (66, (70 - 5, 160 - 10), 4, 1, "#240f00", True),
            (66, (130 + 4, 160 - 5), 6, 1, "#240f00", True)
        ],
    ),
}


def plot_line_segment(
    startpoint_coors, endpoint_coors, colour, linewidth, alpha=1.0
):
    """TODO."""
    plt.plot(
        [startpoint_coors[0], endpoint_coors[0]],
        [startpoint_coors[1], endpoint_coors[1]],
        color=colour,
        linewidth=linewidth,
        alpha=alpha,
    )


def plot_straight_line_by_equation(gradient, intercept, colour, linewidth):
    """TODO."""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + gradient * x_vals
    plt.plot(x_vals, y_vals, color=colour, linewidth=linewidth)


def draw_between_line_segments(
    line_seg_1,
    line_seg_2,
    colour,
    linewidth,
    number_lines_to_draw=68,
    alpha=1.0,
    reverse=False,
):
    """TODO."""
    if reverse:
        xs = np.linspace(line_seg_1[1], line_seg_1[0], num=number_lines_to_draw)
    else:
        xs = np.linspace(line_seg_1[0], line_seg_1[1], num=number_lines_to_draw)
    ys = np.linspace(line_seg_2[1], line_seg_2[0], num=number_lines_to_draw)

    for x, y in zip(xs, ys):
        plot_line_segment(
            x, y, colour=colour, linewidth=linewidth, alpha=alpha
        )


def draw_from_point_to_line_segment(
    point, line_seg, colour, linewidth, number_lines_to_draw=68, alpha=1.0
):
    """TODO."""
    ys = np.linspace(line_seg[0], line_seg[1], num=number_lines_to_draw)
    for y in ys:
        plot_line_segment(
            point, y, colour=colour, linewidth=linewidth, alpha=alpha
        )


def draw_regular_polygon(
    number_sides, centre, radius, rotation_no, colour, lw, alpha, ax
):
    """TODO."""
    # First get the vertex coordinates
    polygon_coors = []
    # Taken and adapted from some code in the 'repolygon' project of this repo
    for vertex in range(1, number_sides + 2):
        factor = 2 * vertex * np.pi / number_sides + np.pi / rotation_no
        # Note: radius == repolygon scale
        polygon_coors.append(
            radius * np.array([np.cos(factor), np.sin(factor)])
            + np.array(centre)
        )

    # Now draw those vertices forming the regular polygon
    polygon = Polygon(
        polygon_coors, fill=False, edgecolor=colour, linewidth=lw, alpha=alpha
    )
    ax.add_patch(polygon)

    # Use this to get the points required for replication The Eternal Band
    # if number_sides == 7:  # to find the heptagon vertices for The Eternal Band
    #    print("Centre is at:", centre)
    #    print("Vertices are at:", polygon_coors)

    return polygon_coors


def draw_across_regular_polygon(
    polygon_centre, polygon_coors, colour, lw, alpha, ax
):
    """TODO."""
    # Note: if polygon is an approximated circle, must approximate circle
    # with the effective number of lines to draw divided by two to get the
    # desired spacing.

    # First strip the final coor. which is the first one duplicated:
    polygon_coors = polygon_coors[:-1]

    # Draw from the centre out to the vertices of the polygon:
    for c in polygon_coors:
        plot_line_segment(
            polygon_centre, c, colour=colour, linewidth=lw, alpha=alpha
        )


def format_grids(ax, grid_colour):
    """TODO."""
    ax.set_axisbelow(True)
    ax.minorticks_on()

    # Set the spacings:
    # Major dividers every 10 points, minor every 1, on the given axis
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Customize the grids
    ax.grid(
        which="major",
        linestyle="-",
        linewidth=0.8,
        color=grid_colour,
        alpha=0.5,
    )
    ax.grid(
        which="minor",
        linestyle="-",
        linewidth=0.5,
        color=grid_colour,
        alpha=0.3,
    )


def pre_format_plot(
    figsize, scale_factor, sketch_params, background_colour, grid_colour
):
    """TODO."""
    # Configure very slightly squiggly lines for a more 'hand-drawn' look!
    # This doesn't seem possible at the moment (without making the code much
    # less clean, at least) for the drawn lines only, it also affects the axes and
    # gridlines etc., but is fun to play around with these parameters to see how
    # it influences the style! Note that the 'xkcd' style uses (1, 100, 2): see
    # https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/pyplot.py
    if sketch_params:
        rcParams["path.sketch"] = sketch_params

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(background_colour)

    # Scale plot limits with figsize so the grid ends up composed of squares:
    if figsize[0] < figsize[1]:
        plot_limits_x = (0, scale_factor)
        plot_limits_y = (0, plot_limits_x[1] * figsize[1] / figsize[0])
    else:
        plot_limits_y = (0, scale_factor)
        plot_limits_x = (0, plot_limits_y[1] * figsize[0] / figsize[1])

    ax.set_xlim(plot_limits_x)
    ax.set_ylim(plot_limits_y)

    format_grids(ax, grid_colour)

    return fig, ax


def post_format_plot(ax, background_colour, view_axes_labels_as_guide=False):
    """TODO."""
    ax.set_facecolor(background_colour)

    # Whilst creating a design, we may want to see the axes labels
    if view_axes_labels_as_guide:
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
    else:
        # Note can't just use ax.axis("off") as it hides the grid too
        for ax_choice in ("x", "y"):
            plt.tick_params(
                axis=ax_choice,
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
                labeltop=False,
                labelleft=False,
                labelright=False,
            )
        ax.set_frame_on(False)
    plt.tight_layout()


def plot_overall_design(
    design_to_draw, output_name, output_dir, view_axes_labels_as_guide=False
):
    """TODO."""
    # Unpack geometrical parameters
    line_coors, coor_pairs_to_join = design_to_draw[:2]

    # Unpack style parameters
    dims, line_params, colour_params, *num_lines_to_draw = design_to_draw[2]

    figsize, scale_factor = dims
    linewidth, line_alpha, sketch_rcparams = line_params

    # TODO add fourth value to all for colour params eventually
    ghost_lines = False
    if len(colour_params) == 4 and colour_params[3]:
        # Option to plot only connections, not lines themselves
        background_colour, grid_colour, default_line_colour = colour_params[:-1]
        ghost_lines = True
    else:
        background_colour, grid_colour, default_line_colour = colour_params


    fig, ax = pre_format_plot(
        figsize, scale_factor, sketch_rcparams, background_colour, grid_colour
    )

    # Get change of colours for given pairs of coors to join, if specified:
    change_of_colour = {}
    if len(design_to_draw) >= 4:
        change_of_colour = design_to_draw[3]
    # Get any optional polygons to draw and then draw them first
    if len(design_to_draw) == 5:
        polygons_to_draw = design_to_draw[4]

        join_across = False  # default

        for polygon in polygons_to_draw:
            if len(polygon) > 5:
                join_across = polygon[5]
                polygon = polygon[:5]

            if join_across:
                coors = draw_regular_polygon(
                    *polygon, linewidth, line_alpha, ax
                )
                # where, as specified below, index 1 is centre and 4 is colour
                draw_across_regular_polygon(
                    polygon[1], coors, polygon[4], linewidth, line_alpha, ax
                )
            else:
                # Plot with same line width and alpha as rest of the design
                draw_regular_polygon(*polygon, linewidth, line_alpha, ax)

    # Plot the lines comprising the design
    for index, line_coor in enumerate(line_coors):
        colour = default_line_colour
        if index in change_of_colour.keys():
            colour = change_of_colour[index]

        # TODO ghost lines code may need extending
        if not ghost_lines:
            plot_line_segment(*line_coor, colour, linewidth, line_alpha)

    # Drawing of equally-spaced lines between given pairs of segments
    for index, pairs in enumerate(coor_pairs_to_join):
        coor_1, coor_2 = pairs

        reverse = False
        if coor_1 < 0:
            coor_1 = abs(coor_1)
            reverse = True
        if coor_2 < 0:
            coor_2 = abs(coor_2)
            reverse = True

        colour = default_line_colour
        if index in change_of_colour.keys():
            colour = change_of_colour[index]
        kwargs = {"alpha": line_alpha}
        if num_lines_to_draw:
            kwargs["number_lines_to_draw"] = num_lines_to_draw[0]

        if isinstance(coor_1, tuple):  # not a line but a single given point
            draw_from_point_to_line_segment(
                coor_1, line_coors[coor_2], colour, linewidth, **kwargs
            )
        else:
            ### TODO MAY NEED TO APPLY REVERSE elsewhere too for generality
            draw_between_line_segments(
                line_coors[coor_1],
                line_coors[coor_2],
                colour,
                linewidth,
                reverse=reverse,
                **kwargs,
            )

    post_format_plot(
        ax,
        background_colour,
        view_axes_labels_as_guide=view_axes_labels_as_guide,
    )
    plt.savefig(
        f"img/{output_dir}/{output_name}.png",
        format="png",
        bbox_inches="tight",
        dpi=1000,
    )
    plt.show()


"""
# Plot all replication designs (separately)
for name in [
    "From Its Center",
    "The Great Breath",
    "Wings of the Wind",
    "Union of Water and Fire II",
    "The Eternal Band",
    "Blue Circle",
]:
    design_to_draw = REPLICATION_DESIGN_PARAMETERS[name]
    plot_overall_design(
        design_to_draw,
        name.replace(" ", "_").lower(),
        "replications",
        # view_axes_labels_as_guide=True
    )
"""

# Then plot all of my own variation designs (also separately)
for name in [
    #"Treble Clef",
    #"Softening",
    #"Crosses on our Eyes",
    "Jaws of Resonance",
    "Owl",
    "Always the Hourglass",
    "Angry Eyes and Mouth of a God",
    "Primitive Surveillance",
]:
    design_to_draw = VARIATION_DESIGN_PARAMETERS[name]
    plot_overall_design(
        design_to_draw,
        name.replace(" ", "_").lower(),
        "variations",
        # view_axes_labels_as_guide=True
    )
