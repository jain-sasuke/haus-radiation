from manim import *
import json
import numpy as np
from pathlib import Path


class RadiationCaseScene(Scene):
    def construct(self):
        case_dir = Path("outputs/medium_threshold")
        summary = json.loads((case_dir / "summary.json").read_text())

        traj = np.load(case_dir / "trajectory.npz")
        prof = np.load(case_dir / "angular_profile.npz")

        # -----------------------------
        # Clean title block
        # -----------------------------
        title = Text(
            "Constant velocity",
            font_size=28,
            weight=NORMAL,
        ).to_edge(UP, buff=0.18)

        subtitle = Text(
            "in medium above threshold",
            font_size=24,
            weight=NORMAL,
        ).next_to(title, DOWN, buff=0.06)

        verdict = Text(
            "Threshold directional case",
            font_size=20,
            color=YELLOW,
            weight=NORMAL,
        ).next_to(subtitle, DOWN, buff=0.10)

        title_group = VGroup(title, subtitle, verdict)
        self.play(FadeIn(title_group))
        self.wait(0.4)

        # -----------------------------
        # Left info panel: smaller, cleaner
        # -----------------------------
        panel = RoundedRectangle(
            width=5.9,
            height=1.95,
            corner_radius=0.16,
            stroke_width=2,
        ).to_corner(UL, buff=0.40).shift(DOWN * 0.95)

        line1 = Text("Trajectory: constant velocity", font_size=18, weight=NORMAL)
        line2 = Text("Medium: nondispersive", font_size=18, weight=NORMAL)
        line3 = Text("Finite-frequency directional", font_size=17, weight=NORMAL)
        line4 = Text("enhancement in medium", font_size=17, weight=NORMAL)

        panel_text = VGroup(line1, line2, line3, line4).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.11
        )

        panel_text.move_to(panel.get_center())
        panel_text.align_to(panel, LEFT).shift(RIGHT * 0.30)

        self.play(Create(panel), FadeIn(panel_text))
        self.wait(0.4)

        # -----------------------------
        # Trajectory plot
        # -----------------------------
        t = traj["t"]
        z = traj["z"]

        zmin = float(np.min(z))
        zmax = float(np.max(z))
        margin = 0.15 * max(1.0, zmax - zmin)

        axes = Axes(
            x_range=[float(np.min(t)), float(np.max(t)), 20],
            y_range=[zmin - margin, zmax + margin, max((zmax - zmin) / 4, 1e-6)],
            x_length=6.8,
            y_length=3.1,
            axis_config={"include_numbers": False},
            tips=True,
        ).move_to(DOWN * 2.0)

        labels = axes.get_axis_labels(
            Text("t", font_size=20, weight=NORMAL),
            Text("z", font_size=20, weight=NORMAL)
        )

        self.play(Create(axes), FadeIn(labels))

        sample_step = max(1, len(t) // 200)
        points = [axes.c2p(float(tt), float(zz)) for tt, zz in zip(t[::sample_step], z[::sample_step])]

        path = VMobject(color=BLUE)
        path.set_points_as_corners(points)

        dot = Dot(points[0], color=RED, radius=0.07)

        self.play(Create(path), FadeIn(dot))
        self.play(MoveAlongPath(dot, path), run_time=4, rate_func=linear)
        self.wait(0.4)

        # -----------------------------
        # Angular profile plot
        # -----------------------------
        theta = prof["theta_grid"]
        profile = prof["profile"]
        if np.max(profile) > 0:
            profile = profile / np.max(profile)

        p_axes = Axes(
            x_range=[0, float(np.max(theta)), 0.5],
            y_range=[0, 1.0, 0.2],
            x_length=4.5,
            y_length=2.4,
            axis_config={"include_numbers": False},
            tips=True,
        ).to_corner(UR, buff=0.45).shift(DOWN * 1.02)

        p_labels = p_axes.get_axis_labels(
            Text("θ", font_size=20, weight=NORMAL),
            Text("S", font_size=20, weight=NORMAL)
        )

        curve = p_axes.plot_line_graph(
            x_values=theta.tolist(),
            y_values=profile.tolist(),
            line_color=GREEN,
            add_vertex_dots=False,
        )

        self.play(Create(p_axes), FadeIn(p_labels))
        self.play(Create(curve))
        self.wait(1.2)