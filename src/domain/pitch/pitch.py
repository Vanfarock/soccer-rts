import math

from infra.engine.primitives.arc import Arc
from infra.engine.primitives.ellipse import Ellipse
from infra.engine.primitives.game_object import GameObject, GameObjectType
from infra.engine.primitives.line import Line
from infra.engine.primitives.rectangle import Rectangle
from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from infra.engine.window import Window
from shared.colors import Color


class Pitch(GameObject):
    WIDTH = 1050
    HEIGHT = 680
    DRAG = 2.5
    PENALTY_BOX_DEPTH = 165
    PENALTY_BOX_WIDTH = 403
    GOAL_AREA_DEPTH = 55
    GOAL_AREA_WIDTH = 183
    GOAL_WIDTH = 73
    CENTER_CIRCLE_RADIUS = 91
    PENALTY_SPOT_DISTANCE = 110
    CORNER_ARC_RADIUS = 10

    def __init__(self, window: Window, margin: int = 40):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=Vector2D(0, 0),
            size=Vector2D(Pitch.WIDTH, Pitch.HEIGHT),
        )
        self._margin = margin
        self._line_width = 1
        self._layout(window.screen.get_size())

    def render(self, target: RenderTarget) -> None:
        target.set_background_color(Color.PITCH_BG)

        Rectangle(
            self.world_to_screen(Vector2D(0, 0)),
            self.world_size_to_screen(Vector2D(Pitch.WIDTH, Pitch.HEIGHT)),
            Color.PITCH_SURFACE,
            thickness=0,
        ).render(target)

        for obj in self._build_linework():
            obj.render(target)

    def _build_linework(self) -> list[GameObject]:
        w = Pitch.WIDTH
        h = Pitch.HEIGHT
        lines: list[GameObject] = []

        corners = [
            Vector2D(0, 0),
            Vector2D(w, 0),
            Vector2D(w, h),
            Vector2D(0, h),
        ]
        for start, end in zip(corners, corners[1:] + corners[:1]):
            lines.append(self._line(start, end))

        mid_x = w / 2
        lines.append(self._line(Vector2D(mid_x, 0), Vector2D(mid_x, h)))

        center = Vector2D(w / 2, h / 2)
        lines.append(
            self._arc(center, Pitch.CENTER_CIRCLE_RADIUS, 0, math.tau, segments=48)
        )
        lines.append(self._spot(center))

        pb_depth = Pitch.PENALTY_BOX_DEPTH
        pb_width = Pitch.PENALTY_BOX_WIDTH
        ga_depth = Pitch.GOAL_AREA_DEPTH
        ga_width = Pitch.GOAL_AREA_WIDTH
        pb_top = (h - pb_width) / 2
        ga_top = (h - ga_width) / 2

        for depth, width, top in (
            (pb_depth, pb_width, pb_top),
            (ga_depth, ga_width, ga_top),
        ):
            lines.extend(
                [
                    self._line(Vector2D(depth, top), Vector2D(depth, top + width)),
                    self._line(Vector2D(0, top), Vector2D(depth, top)),
                    self._line(Vector2D(0, top + width), Vector2D(depth, top + width)),
                ]
            )

        for depth, width, top in (
            (pb_depth, pb_width, pb_top),
            (ga_depth, ga_width, ga_top),
        ):
            right_x = w - depth
            lines.extend(
                [
                    self._line(Vector2D(right_x, top), Vector2D(right_x, top + width)),
                    self._line(Vector2D(w, top), Vector2D(right_x, top)),
                    self._line(
                        Vector2D(w, top + width), Vector2D(right_x, top + width)
                    ),
                ]
            )

        spot_y = h / 2
        spot_dist = Pitch.PENALTY_SPOT_DISTANCE
        arc_radius = Pitch.CENTER_CIRCLE_RADIUS
        box_depth = Pitch.PENALTY_BOX_DEPTH
        half_arc = math.acos((box_depth - spot_dist) / arc_radius)

        for spot_x in (spot_dist, w - spot_dist):
            lines.append(self._spot(Vector2D(spot_x, spot_y)))
            if spot_x < w / 2:
                lines.append(
                    self._arc(
                        Vector2D(spot_x, spot_y),
                        arc_radius,
                        -half_arc,
                        half_arc,
                    )
                )
            else:
                lines.append(
                    self._arc(
                        Vector2D(spot_x, spot_y),
                        arc_radius,
                        math.pi - half_arc,
                        math.pi + half_arc,
                    )
                )

        r = Pitch.CORNER_ARC_RADIUS
        corner_arcs = [
            (Vector2D(r, r), math.pi, 3 * math.pi / 2),
            (Vector2D(w - r, r), 3 * math.pi / 2, math.tau),
            (Vector2D(r, h - r), math.pi / 2, math.pi),
            (Vector2D(w - r, h - r), 0, math.pi / 2),
        ]
        for center, start, stop in corner_arcs:
            lines.append(self._arc(center, r, start, stop, segments=8))

        goal_half = Pitch.GOAL_WIDTH / 2
        center_y = h / 2
        depth = 8
        lines.extend(
            [
                self._rect(-depth, center_y - goal_half, depth, Pitch.GOAL_WIDTH),
                self._rect(w, center_y - goal_half, depth, Pitch.GOAL_WIDTH),
            ]
        )

        return lines

    def _layout(self, screen_size: tuple[int, int]) -> None:
        sw, sh = screen_size
        scale = min(
            (sw - 2 * self._margin) / Pitch.WIDTH,
            (sh - 2 * self._margin) / Pitch.HEIGHT,
        )
        offset = Vector2D(
            (sw - Pitch.WIDTH * scale) / 2,
            (sh - Pitch.HEIGHT * scale) / 2,
        )
        self.set_transform(scale, offset)
        self._line_width = max(1, round(2 * scale))

    def _line(self, start: Vector2D, end: Vector2D) -> Line:
        return Line(
            self.world_to_screen(start),
            self.world_to_screen(end),
            Color.WHITE,
            self._line_width,
        )

    def _spot(self, center: Vector2D, radius: float = 3) -> Ellipse:
        diameter = self.world_size_to_screen(Vector2D(radius * 2, radius * 2)).x
        top_left = self.world_to_screen(Vector2D(center.x - radius, center.y - radius))
        return Ellipse(top_left, Vector2D(diameter, diameter), Color.WHITE)

    def _arc(
        self,
        center: Vector2D,
        radius: float,
        start_angle: float,
        stop_angle: float,
        *,
        segments: int = 48,
    ) -> Arc:
        return Arc(
            self.world_to_screen(center),
            self.world_size_to_screen(Vector2D(radius, radius)).x,
            start_angle,
            stop_angle,
            Color.WHITE,
            self._line_width,
            segments=segments,
        )

    def _rect(self, x: float, y: float, w: float, h: float) -> Rectangle:
        return Rectangle(
            self.world_to_screen(Vector2D(x, y)),
            self.world_size_to_screen(Vector2D(w, h)),
            Color.WHITE,
            thickness=0,
        )
