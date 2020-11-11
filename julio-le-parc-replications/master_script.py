import itertools

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms

import numpy as np


"""
References (all from The Metropolitan Museum of Art)

* Mutation of Forms (1959):
    https://www.metmuseum.org/art/collection/search/815337
* Rotations (1959):
    https://www.metmuseum.org/art/collection/search/815346
* Rotation of Fractioned Circles (1959):
    https://www.metmuseum.org/art/collection/search/815341
* Rotation in Red and Black (1959):
    https://www.metmuseum.org/art/collection/search/815338

See also the Le Parc's website:
    http://www.julioleparc.org/
"""


IMAGE_PAD_POINTS = 2


class LeParcDesign:
    """ TODO.
    """

    def __init__(self, design_name, gridpoints, colours):
        self.axes = None  # to be set
        self.design_name = design_name
        self.gridpoints = gridpoints
        self.colours = colours
        self.background_colour = "antiquewhite"  # sensible pan-design default

    def create_design():
        """ TODO. """
        raise NotImplementedError("Designs must be created by subclassing.")

    def format_canvas(self):
        """ Format canvas to centre on image with no visible axes markings. """
        fig, ax = plt.subplots(figsize=(6, 6))
        self.axes = ax
        self.create_design()
        
        fig.set_canvas(plt.gcf().canvas)
        self.background_colour = self.colours["OFF WHITE"]
        fig.patch.set_facecolor(self.background_colour)
        padding_per_side = 2
        limits = (
            self.gridpoints - padding_per_side,
            self.gridpoints + padding_per_side
        )

        ax.set_xlim(*limits)
        ax.set_ylim(*limits)

        plt.axis('equal')
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()

    def plot_and_save_design(self):
        background_colour = self.format_canvas()

        save_to_dir = self.design_name.lower().replace(" ", "_")
        # For creating unique names to save generated variations whilst trying
        # to get the angles the same as the original(!):
        # # import uuid
        plt.savefig(
            'img/{}/replication_of_original.png'.format(save_to_dir),
            # # 'img/rotation_in_red_and_black/misc_variations/'
            # # '{}.png'.format(uuid.uuid4()),
            format='png',
            bbox_inches='tight',
            facecolor=self.background_colour,
        )


class Mutations(LeParcDesign):
    """ TODO.
    """

    def __init__(self):
        self.design_name = "MUTATION OF FORMS"
        self.gridpoints = 10
        self.colours = {
            "OFF WHITE": "#FAEFDD",
            "RED": "#CB0B22",
            "BLUE": "#1D119B",
        }

    @staticmethod
    def create_mutations_linspaced_angles(
            max_coverage, min_coverage, number_points_per_side):
        """ TODO.

        NOTE: angles start pointing downwards i.e. 0 degs is south in PyPlot.
        So red wedges are constrained to -135 to +45, blues to +45 to +225.

        Original design angular coverage pattern is:

             max blue ............. min blue
             min red  .............  max red
             ..            ..             ..
             ..            ..             ..
             ...........half blue...........
             ...........half red............
             ..            ..             ..
             ..            ..             ..
             min blue ............. max blue
             max red  .............  min red

        Define max and min angular coverages for the wedges:
        * red wedges go from -135 <- -45 -> +45
        * blue wedges go from +45 <- +135 -> +225
        """

        # Use linspace to get 1D arrays of angles evenly spaced across coverage:
        theta1_min_to_max = np.linspace(
            max_coverage[0], min_coverage[0], num=number_points_per_side)
        theta2_min_to_max = np.linspace(
            max_coverage[1], min_coverage[1], num=number_points_per_side)

        return np.column_stack((theta1_min_to_max, theta2_min_to_max))

    @staticmethod
    def plot_mutations_wedge(centre, theta1, theta2, colour):
        """ TODO. """
        # 0.5 radius means the circles containing the wedges just touch their
        # neighbours. Use 0.475 radius to provide a small gap as per the design.
        return mpatches.Wedge(
            centre, 0.475, theta1, theta2, color=colour
        )

    def plot_mutations_wedges(
            self, position, wedge_1_thetas, wedge_2_thetas, colour_1,
            colour_2
    ):
        """ TODO. """
        wedge_1 = self.plot_mutations_wedge(
            position, *wedge_1_thetas, colour_1)
        wedge_2 = self.plot_mutations_wedge(
            position, *wedge_2_thetas, colour_2)
        return wedge_1, wedge_2

    def create_mutation_angles_array(
            self, grid_indices, is_red=True, number_points_per_side=5):
        """ TODO. """
        red_max = (-135, 45)
        red_min = (-45, -45)
        blue_max = (45, 225)
        blue_min = (135, 135)

        angles_array = np.zeros(
            (number_points_per_side, number_points_per_side),
            dtype=(float, 2)
        )

        if is_red:
            index = 1  # don't change the spaced_thetas array later (c.f. -1)
            spaced_thetas = self.create_mutations_linspaced_angles(
                max_coverage=red_max, min_coverage=red_min,
                number_points_per_side=number_points_per_side,
            )
        else:
            index = -1  # to reverse the spaced_thetas array later, via [::-1]
            spaced_thetas = self.create_mutations_linspaced_angles(
                max_coverage=blue_max, min_coverage=blue_min,
                number_points_per_side=number_points_per_side,
            )

        # 1. Make first and last column correct:
        for j in grid_indices:
            angles_array[0][j] = spaced_thetas[::index][j]
            angles_array[-1][j] = spaced_thetas[::index][-j-1]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in grid_indices:
            row_angles = self.create_mutations_linspaced_angles(
                max_coverage=angles_array[0][i],
                min_coverage=angles_array[-1][i],
                number_points_per_side=number_points_per_side,
            )
            angles_array[i] = row_angles

        return angles_array

    def create_design(self):
        """ TODO. """
        grid_points = range(self.gridpoints)

        # Calculate angles:
        red_angles_array = self.create_mutation_angles_array(
            is_red=True, grid_indices=grid_points,
            number_points_per_side=self.gridpoints
        )
        blue_angles_array = self.create_mutation_angles_array(
            is_red=False, grid_indices=grid_points,
            number_points_per_side=self.gridpoints
        )
        for i, j in itertools.product(grid_points, grid_points):
            # Get angles:
            red_thetas = red_angles_array[i][j]
            blue_thetas = blue_angles_array[i][j]

            # Now create and plot the wedges onto the canvas:
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            red_wedge, blue_wedge = self.plot_mutations_wedges(
                position_xy, red_thetas, blue_thetas,
                colour_1=self.colours["RED"],
                colour_2=self.colours["BLUE"],
            )
            self.axes.add_patch(red_wedge)
            self.axes.add_patch(blue_wedge)


class Rotations(LeParcDesign):
    """ TODO.
    """

    def __init__(self): 
        self.design_name = "ROTATIONS"
        self.gridpoints = 13
        self.colours = {
            "OFF WHITE": "#F4EDE5",
            "OFF BLACK": "#161815",
        }

    @staticmethod
    def create_rotations_angles_array(
            grid_indices, number_points_per_side=5):
        """ TODO. """
        angles_array = np.zeros(
            (number_points_per_side, number_points_per_side),
            dtype=float
        )

        spaced_thetas = np.linspace(0, 180, number_points_per_side)
        # 1. Make first and last column correct:
        for j in grid_indices:
            angles_array[0][j] = spaced_thetas[j]
            angles_array[-1][j] = spaced_thetas[-j-1]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in grid_indices:
            # Minus sign is to achieve clockwise angle changes as per the design.
            # Without it the angles would move from the first to the last angles
            # in an anti-clockwise direction:
            row_angles = np.linspace(
                -1 * angles_array[0][i],  # see above regarding -1 factor
                angles_array[-1][i],
                number_points_per_side,
            )
            angles_array[i] = row_angles

        return angles_array

    @staticmethod
    def plot_rotations_patch(
            centre, rect_angle, foreground_colour, background_colour, ax):
        """ TODO. """
        # These parameters are adapted to match the original design:
        radius = 0.45
        offset_amount = 0.3
        padding = 0.03

        # Note: get a very thin but still visible edge line on circle even if set
        # linewidth to zero, so to workaround make edgecolour background colour.
        patch = mpatches.Circle(
            centre, radius, facecolor=foreground_colour,
            edgecolor=background_colour,
        )
        # The clipping rectangle, rotated appropriately (no need to rotate circle!)
        clip_patch = mpatches.Rectangle(
            (centre[0] + offset_amount, centre[1] - radius),
            radius - offset_amount + padding,
            2 * radius, color=background_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle) + ax.transData
        )
        return (patch, clip_patch)

    def create_design(self):
        """ TODO. """
        grid_points = range(self.gridpoints)

        angles_array = self.create_rotations_angles_array(
            grid_points,
            number_points_per_side=self.gridpoints
        )
        for i, j in itertools.product(grid_points, grid_points):
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            circle, clipping_rectangle = self.plot_rotations_patch(
                position_xy,
                angles_array[i][j],
                self.colours["OFF BLACK"],
                self.colours["OFF WHITE"],
                self.axes,
            )
            self.axes.add_patch(circle)
            clipping_rectangle.set_clip_path(circle)
            self.axes.add_patch(clipping_rectangle)


class Fractioned(LeParcDesign):
    """ TODO.
    """

    def __init__(self): 
        self.design_name = "ROTATION OF FRACTIONED CIRCLES"
        self.gridpoints = 9
        self.colours = {
            "OFF WHITE": "#F5EFE3",
            "LIGHT GREY": "#D3D2D0",
            "DARK GREY": "#63676B",
        }

    @staticmethod
    def create_fractioned_angles_array(
            grid_indices, number_points_per_side):
        """ TODO. """

        angles_array = np.zeros(
            (number_points_per_side, number_points_per_side),
            dtype=float
        )

        first_col_thetas = np.linspace(-70, 70, number_points_per_side)
        last_col_thetas = np.linspace(70, 3 * 360 + 290, number_points_per_side)

        # 1. Make first and last column correct:
        for j in grid_indices:
            angles_array[0][j] = first_col_thetas[j]
            angles_array[-1][j] = last_col_thetas[j]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in grid_indices:
            row_angles = np.linspace(
                angles_array[0][i],
                angles_array[-1][i],
                number_points_per_side,
            )
            angles_array[i] = row_angles

        return -1 * np.flip(angles_array, axis=1)

    @staticmethod
    def plot_fractioned_circle_patch(
            centre, rect_angle, dark_colour, light_colour, background_colour, ax):
        """ TODO. """
        # These parameters are adapted to match the original design:
        radius = 0.45
        offset_amount = 0.02
        light_offset = 0.5
        padding = 0.03
        line_size = 0.12

        # Note: get a very thin but still visible edge line on circle even if set
        # linewidth to zero, so to workaround make edgecolour background colour.
        light_patch = mpatches.Circle(
            centre, radius, facecolor=light_colour,
            edgecolor=background_colour,
        )
        start_at = (centre[0] + offset_amount, centre[1] - radius)
        clip_alpha = 3
        # The clipping rectangle, rotated appropriately (no need to rotate circle!)
        clip_patch = mpatches.Rectangle(
            start_at,
            line_size,
            2 * radius, color=background_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle) + ax.transData,
            alpha=clip_alpha
        )
        dark_patch = mpatches.Rectangle(
            start_at,
            radius,
            2 * radius, color=dark_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle) + ax.transData,
            alpha=clip_alpha - 1,
        )
        return (dark_patch, light_patch, clip_patch)

    def create_design(self):
        """ TODO. """
        grid_points = range(self.gridpoints)

        angles_array = self.create_fractioned_angles_array(
            grid_points,
            number_points_per_side=self.gridpoints
        )
        for i, j in itertools.product(grid_points, grid_points):
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            dark_cir, light_cir, off_white_line = self.plot_fractioned_circle_patch(
                position_xy,
                angles_array[i][j],
                self.colours["DARK GREY"],
                self.colours["LIGHT GREY"],
                self.colours["OFF WHITE"],
                self.axes,
            )
            self.axes.add_patch(light_cir)
            dark_cir.set_clip_path(light_cir)
            self.axes.add_patch(dark_cir)
            off_white_line.set_clip_path(light_cir)
            self.axes.add_patch(off_white_line)


class RedAndBlack(LeParcDesign):
    """ TODO.
    """

    def __init__(self): 
        self.design_name = "ROTATION IN RED AND BLACK"
        self.gridpoints = 10
        self.colours = {
            "OFF WHITE": "#F2ECE0",
            "OFF BLACK": "#100F0D",
            "RED": "#983134",
        }

    @staticmethod
    def create_red_and_black_angles_array(
            grid_indices, number_points_per_side):
        """ TODO. """

        angles_array = np.zeros(
            (number_points_per_side, number_points_per_side),
            dtype=float
        )

        # Alternate between +45 and -45, but with a different start point for each:
        first_col_thetas = np.full((number_points_per_side), 45)
        first_col_thetas[1::2] = -45  # starts with 45 (then -45 is next, etc.)
        last_col_thetas = np.full((number_points_per_side), 45)
        last_col_thetas[::2] = -45  # starts with -45

        # 1. Make first and last column correct:
        angles_array[0] = first_col_thetas
        angles_array[-1] = last_col_thetas

        # 2. Create rows linearly-spaced based on first and last columns. In this
        #    case, a cycle factor sets how many rotations from angles A to B.
        for i in grid_indices:
            use_cycle_factor = (i // 2) + 7
            normalised_angles_a = angles_array[0][i]
            normalised_angles_b = angles_array[-1][i] + 360 * use_cycle_factor
            row_angles = np.linspace(
                normalised_angles_a,
                normalised_angles_b,
                number_points_per_side,
            )
            angles_array[:, i] = row_angles

        return angles_array

    @staticmethod
    def create_cross_line(ax, centre, length, width, colour, angle, zorder):
        """ TODO. """
        lines = []
        for theta in (angle, angle + 180):  # two parallel half-lines from centre
            lines.append(
                mpatches.Rectangle(
                    (centre[0] - width, centre[1] - (width / 2.0)),  # normalised
                    length, width, color=colour,
                    transform=mtransforms.Affine2D().rotate_deg_around(
                        *centre, theta) + ax.transData, zorder=zorder
                )
            )
        return lines

    def plot_simple_cross(self, centre, base_theta, colour_1, colour_2, ax):
        """ TODO. """
        half_length = 0.5
        width = 0.05

        # Define two lines perpendicular to each other as patches
        reference_zorder = 1
        cross_lines = (
            self.create_cross_line(
                ax, centre, half_length, width, colour_1, base_theta,
                reference_zorder
            ) +
            self.create_cross_line(
                ax, centre, half_length, width, colour_2, base_theta + 90,
                reference_zorder - 10  # i.e. this line is shown on top
            )
        )

        return cross_lines

    def create_design(self):
        """ TODO. """
        grid_points = range(self.gridpoints)

        # TODO: using RoFC angles array as a placeholder. Find actual!
        angles_array = self.create_red_and_black_angles_array(
            grid_points,
            number_points_per_side=self.gridpoints
        )
        for i, j in itertools.product(grid_points, grid_points):
            # Now create and plot the wedges onto the canvas:
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            line_patches = self.plot_simple_cross(
                position_xy, angles_array[i][j],
                self.colours["RED"],
                self.colours["OFF BLACK"],
                self.axes
            )
            for line in line_patches:
                self.axes.add_patch(line)


# Plot and show all four designs
for design_class in [Mutations, Rotations, Fractioned, RedAndBlack]:
    design_class().plot_and_save_design()
plt.show()
