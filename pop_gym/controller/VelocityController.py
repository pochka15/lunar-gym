import numpy as np
from math import cos, sin
from dataclasses import dataclass
from typing import Optional
from controller.Controller import Controller
from others.State import State, LEFT_ACTION, RIGHT_ACTION, UP_ACTION, IDLE_ACTION


@dataclass
class VelocityControllerConfig:
    max_y_velocity: float
    max_priority: float

    def __str__(self):
        return f"""
VelocityControllerConfig
  - max_y_velocity: {self.max_y_velocity}
  - max_priority: {self.max_priority}"""


class VelocityController(Controller):
    """
    It tries to slow down the lunar in case it has too high y velocity.
    This controller finds an opposite vector to the current velocity vector
    and acts towards this opposite vector.
    """

    def __init__(self, config: VelocityControllerConfig, log):
        self.log = log
        self.config = config

    def handle_state(self, state: State):
        pass

    @property
    def action(self):
        """See the https://keisan.casio.com/exec/system/1223522781"""

        if self.log[-1] is None or self.log[-2] is None:
            return IDLE_ACTION

        # inverted velocity vector
        vec = -self.log[-1].velocity

        multipliers = [cos(self.log[-1].angle), sin(self.log[-1].angle)]
        x = np.sum(vec * multipliers)

        multipliers = [-sin(self.log[-1].angle), cos(self.log[-1].angle)]
        y = np.sum(vec * multipliers)

        if x >= 0:
            return RIGHT_ACTION if x >= y else UP_ACTION
        else:
            return LEFT_ACTION if -x >= y else UP_ACTION

    @property
    def priority(self):
        if len(self.log) < 2:
            return 0

        if self.has_high_acceleration:
            return self.config.max_priority

        vy = self.log[-1].velocity[1]
        return self.config.max_priority / 2 if abs(vy) > self.config.max_y_velocity else 0

    @property
    def has_high_acceleration(self):
        distance = 2
        if len(self.log) < distance:
            return False

        lhs = abs(self.log[-1].position)
        rhs = abs(self.log[-distance].position)
        diff = (abs(lhs - rhs) * [1000, 1000])
        if diff[0] > 9 or diff[1] > 9:
            return True
        return False
