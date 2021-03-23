from abc import ABCMeta, abstractmethod
import itertools

import matplotlib.animation as animation
import matplotlib.pyplot as plt
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


class LeParcDesign(metaclass=ABCMeta):
    """TODO."""

    def __init__(self, design_name, gridpoints, colours):
        self.design_name = design_name
        self.gridpoints = gridpoints
        self.grid_indices = range(self.gridpoints)
        self.colours = colours
        self.background_colour = None

        fig, ax = plt.subplots(figsize=(6, 6))
        self.fig = fig
        self.axes = ax
        self.fig.set_canvas(plt.gcf().canvas)
        self.format_plt()
        self.patches = None

        self.save_to_dir = self.design_name.lower().replace(" ", "_")

        self.angles_array = self.create_design_angles_array()

        self.ABC_error_msg = "Designs must be created by subclassing."

    @abstractmethod
    def create_design_patches_per_gridpoint(self):
        """ TODO. """
        raise NotImplementedError(self.ABC_error_msg)

    @abstractmethod
    def create_design_angles_array(self):
        """ TODO. """
        raise NotImplementedError(self.ABC_error_msg)

    @abstractmethod
    def create_design(self):
        """ TODO. """
        raise NotImplementedError(self.ABC_error_msg)

    def format_canvas(self):
        """ Format canvas to centre on image with no visible axes markings. """
        self.background_colour = self.colours["OFF WHITE"]
        self.fig.patch.set_facecolor(self.background_colour)
        padding_per_side = 2
        limits = (
            self.gridpoints - padding_per_side,
            self.gridpoints + padding_per_side,
        )

        self.axes.set_xlim(*limits)
        self.axes.set_ylim(*limits)

    def format_plt(self):
        """ TODO. """
        # Note: use this instead of plt.axis('equal') since due to the
        # rotation of outer patches in the animation, 'equal' will vary
        # somewhat and therefore the whole animation will shift and re-size
        # slightly otherwise, but want all patches fixed in position.
        min_point = 1
        max_point = self.gridpoints + 2  # +2 to pad by 1 on each side
        plt.axis([min_point, max_point, min_point, max_point])

        plt.axis("off")
        plt.xticks([])
        plt.yticks([])

    def plot_and_save_design(self):
        """ TODO. """
        self.format_canvas()
        self.create_design()
        self.format_plt()

        plt.tight_layout()

        # For creating unique names to save generated variations whilst trying
        # to get the angles the same as the original(!):
        # # import uuid
        plt.savefig(
            "img/{}/replication_of_original.png".format(self.save_to_dir),
            # # 'img/rotation_in_red_and_black/misc_variations/'
            # # '{}.png'.format(uuid.uuid4()),
            format="png",
            bbox_inches="tight",
            facecolor=self.background_colour,
        )

    def init_animated_design(self):
        """ TODO. """
        self.create_design()
        self.format_plt()

    def update_animation_for_uniform_rotation(self, i):
        """ TODO. """
        # !!!
        # TODO: this code as-is is not at all efficient since it is
        # re-generating the same patches, but at different collective
        # rotations, for every single frame. Instead retain the patches
        # created the first time and continuously update here the rotation
        # only via setting the relevant properties on those.
        # !!!
        self.axes.cla()
        self.angles_array = (
            self.create_design_angles_array() + 10 * i * np.pi / 12
        )
        self.create_design()
        self.format_plt()

    def plot_and_save_animated_design(self):
        """ TODO. """
        self.format_canvas()

        # Note: increase *frames* for longer video, decrease *interval* and/or
        # addition to angles_array to make the video smoother (less choppy)
        anim = animation.FuncAnimation(
            self.fig,
            self.update_animation_for_uniform_rotation,
            init_func=self.init_animated_design,
            interval=5,
            frames=240,
        )
        plt.tight_layout()

        # Note (see also above comment): increase *fps* to speed up the video
        anim.save(
            "img/{}/animation_with_uniform_rotation.mp4".format(
                self.save_to_dir
            ),
            writer=animation.FFMpegWriter(
                fps=30, extra_args=["-vcodec", "libx264"]
            ),
        )


class Mutations(LeParcDesign):
    """TODO."""

    def __init__(self):
        super().__init__(
            "MUTATION OF FORMS",
            10,
            {
                "OFF WHITE": "#FAEFDD",
                "RED": "#CB0B22",
                "BLUE": "#1D119B",
            },
        )

        self.red_angles_array = self.angles_array  # from parent LeParcDesign
        self.blue_angles_array = self.create_design_angles_array(is_red=False)

    @staticmethod
    def plot_mutations_wedge(centre, theta1, theta2, colour):
        """ TODO. """
        # 0.5 radius means the circles containing the wedges just touch their
        # neighbours. Use 0.475 to provide a small gap as per the design.
        return mpatches.Wedge(centre, 0.475, theta1, theta2, color=colour)

    def create_design_patches_per_gridpoint(
        self, position, wedge_1_thetas, wedge_2_thetas, colour_1, colour_2
    ):
        """ TODO. """
        wedge_1 = self.plot_mutations_wedge(
            position, *wedge_1_thetas, colour_1
        )
        wedge_2 = self.plot_mutations_wedge(
            position, *wedge_2_thetas, colour_2
        )
        return wedge_1, wedge_2

    def create_mutations_linspaced_angles(self, max_coverage, min_coverage):
        """TODO.

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

        # Use linspace for 1D arrays of angles evenly spaced across coverage.
        theta1_min_to_max = np.linspace(
            max_coverage[0], min_coverage[0], num=self.gridpoints
        )
        theta2_min_to_max = np.linspace(
            max_coverage[1], min_coverage[1], num=self.gridpoints
        )

        return np.column_stack((theta1_min_to_max, theta2_min_to_max))

    def create_design_angles_array(self, is_red=True):
        """ TODO. """
        red_max = (-135, 45)
        red_min = (-45, -45)
        blue_max = (45, 225)
        blue_min = (135, 135)

        angles_array = np.zeros(
            (self.gridpoints, self.gridpoints), dtype=(float, 2)
        )

        if is_red:
            index = 1  # don't change the spaced_thetas array later (c.f. -1)
            spaced_thetas = self.create_mutations_linspaced_angles(
                max_coverage=red_max, min_coverage=red_min
            )
        else:
            index = -1  # to reverse the spaced_thetas array later, via [::-1]
            spaced_thetas = self.create_mutations_linspaced_angles(
                max_coverage=blue_max, min_coverage=blue_min
            )

        # 1. Make first and last column correct:
        for j in self.grid_indices:
            angles_array[0][j] = spaced_thetas[::index][j]
            angles_array[-1][j] = spaced_thetas[::index][-j - 1]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in self.grid_indices:
            row_angles = self.create_mutations_linspaced_angles(
                max_coverage=angles_array[0][i],
                min_coverage=angles_array[-1][i],
            )
            angles_array[i] = row_angles

        return angles_array

    def create_design(self):
        """ TODO. """
        for i, j in itertools.product(self.grid_indices, self.grid_indices):
            # Get angles:
            red_thetas = self.red_angles_array[i][j]
            blue_thetas = self.blue_angles_array[i][j]

            # Now create and plot the wedges onto the canvas:
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            red_wedge, blue_wedge = self.create_design_patches_per_gridpoint(
                position_xy,
                red_thetas,
                blue_thetas,
                colour_1=self.colours["RED"],
                colour_2=self.colours["BLUE"],
            )
            self.axes.add_patch(red_wedge)
            self.axes.add_patch(blue_wedge)

    def update_animation_for_uniform_rotation(self, i):
        """ TODO. """
        self.axes.cla()

        # In this case there are two angles (red and blue) that need updating
        angle_addition_per_frame = 10 * i * np.pi / 12
        self.red_angles_array = (
            self.create_design_angles_array() + angle_addition_per_frame
        )
        self.blue_angles_array = (
            self.create_design_angles_array(is_red=False)
            + angle_addition_per_frame
        )

        self.create_design()
        self.format_plt()


class Rotations(LeParcDesign):
    """TODO."""

    def __init__(self):
        super().__init__(
            "ROTATIONS",
            13,
            {
                "OFF WHITE": "#F4EDE5",
                "OFF BLACK": "#161815",
            },
        )

    def create_design_patches_per_gridpoint(
        self, centre, rect_angle, foreground_colour, background_colour
    ):
        """ TODO. """
        # These parameters are adapted to match the original design:
        radius = 0.45
        offset_amount = 0.3
        padding = 0.03

        # Note: get a very thin but still visible edge to circle even if set
        # linewidth to zero, so (workaround) make edgecolour background colour.
        patch = mpatches.Circle(
            centre,
            radius,
            facecolor=foreground_colour,
            edgecolor=background_colour,
        )
        # The clipping rectangle, rotated appropriately.
        clip_patch = mpatches.Rectangle(
            (centre[0] + offset_amount, centre[1] - radius),
            radius - offset_amount + padding,
            2 * radius,
            color=background_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle
            )
            + self.axes.transData,
        )
        return (patch, clip_patch)

    def create_design_angles_array(self):
        """ TODO. """
        angles_array = np.zeros(
            (self.gridpoints, self.gridpoints), dtype=float
        )

        spaced_thetas = np.linspace(0, 180, self.gridpoints)
        # 1. Make first and last column correct:
        for j in self.grid_indices:
            angles_array[0][j] = spaced_thetas[j]
            angles_array[-1][j] = spaced_thetas[-j - 1]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in self.grid_indices:
            # Minus sign is to achieve clockwise angle changes when going from
            # the first to the last item in the array, as per the design.
            row_angles = np.linspace(
                -1 * angles_array[0][i],  # see above regarding -1 factor
                angles_array[-1][i],
                self.gridpoints,
            )
            angles_array[i] = row_angles

        return angles_array

    def create_design(self, angles_array=None):
        """ TODO. """
        if angles_array is None:
            angles_array = self.angles_array

        for i, j in itertools.product(self.grid_indices, self.grid_indices):
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            circle, clip_rectangle = self.create_design_patches_per_gridpoint(
                position_xy,
                self.angles_array[i][j],
                self.colours["OFF BLACK"],
                self.colours["OFF WHITE"],
            )
            self.axes.add_patch(circle)
            clip_rectangle.set_clip_path(circle)
            self.axes.add_patch(clip_rectangle)


class Fractioned(LeParcDesign):
    """TODO."""

    def __init__(self):
        super().__init__(
            "ROTATION OF FRACTIONED CIRCLES",
            9,
            {
                "OFF WHITE": "#F5EFE3",
                "LIGHT GREY": "#D3D2D0",
                "DARK GREY": "#63676B",
            },
        )

    def create_design_patches_per_gridpoint(
        self, centre, rect_angle, dark_colour, light_colour, background_colour
    ):
        """ TODO. """
        # These parameters are adapted to match the original design:
        radius = 0.45
        offset_amount = 0.02
        line_size = 0.12

        # Note: get a very thin but still visible edge to circle even if set
        # linewidth to zero, so (workaround) make edgecolour background colour.
        light_patch = mpatches.Circle(
            centre,
            radius,
            facecolor=light_colour,
            edgecolor=background_colour,
        )
        start_at = (centre[0] + offset_amount, centre[1] - radius)
        clip_alpha = 3
        # The clipping rectangle, rotated appropriately.
        clip_patch = mpatches.Rectangle(
            start_at,
            line_size,
            2 * radius,
            color=background_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle
            )
            + self.axes.transData,
            alpha=clip_alpha,
        )
        dark_patch = mpatches.Rectangle(
            start_at,
            radius,
            2 * radius,
            color=dark_colour,
            transform=mtransforms.Affine2D().rotate_deg_around(
                *centre, rect_angle
            )
            + self.axes.transData,
            alpha=clip_alpha - 1,
        )
        return (dark_patch, light_patch, clip_patch)

    def create_design_angles_array(self):
        """ TODO. """

        angles_array = np.zeros(
            (self.gridpoints, self.gridpoints), dtype=float
        )

        first_col_thetas = np.linspace(-70, 70, self.gridpoints)
        last_col_thetas = np.linspace(70, 3 * 360 + 290, self.gridpoints)

        # 1. Make first and last column correct:
        for j in self.grid_indices:
            angles_array[0][j] = first_col_thetas[j]
            angles_array[-1][j] = last_col_thetas[j]
        # 2. Create rows linearly-spaced based on first and last columns:
        for i in self.grid_indices:
            row_angles = np.linspace(
                angles_array[0][i],
                angles_array[-1][i],
                self.gridpoints,
            )
            angles_array[i] = row_angles

        return -1 * np.flip(angles_array, axis=1)

    def create_design(self, angles_array=None):
        """ TODO. """
        if angles_array is None:
            angles_array = self.angles_array

        for i, j in itertools.product(self.grid_indices, self.grid_indices):
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            design_patches = self.create_design_patches_per_gridpoint(
                position_xy,
                self.angles_array[i][j],
                self.colours["DARK GREY"],
                self.colours["LIGHT GREY"],
                self.colours["OFF WHITE"],
            )
            dark_cir, light_cir, off_white_line = design_patches
            self.axes.add_patch(light_cir)
            dark_cir.set_clip_path(light_cir)
            self.axes.add_patch(dark_cir)
            off_white_line.set_clip_path(light_cir)
            self.axes.add_patch(off_white_line)


class RedAndBlack(LeParcDesign):
    """TODO."""

    def __init__(self):
        super().__init__(
            "ROTATION IN RED AND BLACK",
            10,
            {
                "OFF WHITE": "#F2ECE0",
                "OFF BLACK": "#100F0D",
                "RED": "#983134",
            },
        )

    def create_design_patches_per_gridpoint(
        self, centre, base_theta, colour_1, colour_2
    ):
        """ TODO. """
        half_length = 0.5
        width = 0.05

        # Define two lines perpendicular to each other as patches
        reference_zorder = 1
        cross_lines = self.create_cross_line(
            centre, half_length, width, colour_1, base_theta, reference_zorder
        ) + self.create_cross_line(
            centre,
            half_length,
            width,
            colour_2,
            base_theta + 90,
            reference_zorder - 10,  # i.e. this line is shown on top
        )

        return cross_lines

    def create_cross_line(self, centre, length, width, colour, angle, zorder):
        """ TODO. """
        lines = []
        for theta in (angle, angle + 180):  # parallel half-lines from centre
            # Centre is normalised with respect to the gridpoint
            lines.append(
                mpatches.Rectangle(
                    (centre[0] - width, centre[1] - (width / 2.0)),  # as above
                    length,
                    width,
                    color=colour,
                    transform=mtransforms.Affine2D().rotate_deg_around(
                        *centre, theta
                    )
                    + self.axes.transData,
                    zorder=zorder,
                )
            )
        return lines

    def create_design_angles_array(self):
        """ TODO. """
        angles_array = np.zeros(
            (self.gridpoints, self.gridpoints), dtype=float
        )

        # Alternate between +45 and -45 but with a different start point
        first_col_thetas = np.full((self.gridpoints), 45)
        first_col_thetas[1::2] = -45  # starts with 45 (then -45 is next, etc.)
        last_col_thetas = np.full((self.gridpoints), 45)
        last_col_thetas[::2] = -45  # starts with -45

        # 1. Make first and last column correct:
        angles_array[0] = first_col_thetas
        angles_array[-1] = last_col_thetas

        # 2. Create rows linearly-spaced based on first and last columns,
        #    where a cycle factor sets how many rotations from angles A to B.
        for i in self.grid_indices:
            use_cycle_factor = (i // 2) + 7
            normalised_angles_a = angles_array[0][i]
            normalised_angles_b = angles_array[-1][i] + 360 * use_cycle_factor
            row_angles = np.linspace(
                normalised_angles_a,
                normalised_angles_b,
                self.gridpoints,
            )
            angles_array[:, i] = row_angles

        return angles_array

    def create_design(self, angles_array=None):
        """ TODO. """
        if angles_array is None:
            angles_array = self.angles_array

        for i, j in itertools.product(self.grid_indices, self.grid_indices):
            # Now create and plot the wedges onto the canvas:
            position_xy = (IMAGE_PAD_POINTS + i, IMAGE_PAD_POINTS + j)
            line_patches = self.create_design_patches_per_gridpoint(
                position_xy,
                self.angles_array[i][j],
                self.colours["RED"],
                self.colours["OFF BLACK"],
            )
            for line in line_patches:
                self.axes.add_patch(line)


# Plot and show all four designs as both the static originals and as
# animated videos where the patches all rotate uniformly:
for design_class in [Mutations, Rotations, Fractioned, RedAndBlack]:
    design_class().plot_and_save_design()
    design_class().plot_and_save_animated_design()

plt.show()
