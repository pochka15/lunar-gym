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

    def __init__(self, config: VelocityControllerConfig):
        self.prev_state_: Optional[State] = None
        self.cur_state_: Optional[State] = None
        self.config = config

    def handle_state(self, state: State):
        self.prev_state_ = self.cur_state_
        self.cur_state_ = state

    @property
    def action(self):
        """See the https://keisan.casio.com/exec/system/1223522781"""

        if self.cur_state_ is None or self.prev_state_ is None:
            return IDLE_ACTION

        # inverted velocity vector
        vec = -self.cur_state_.velocity

        multipliers = [cos(self.cur_state_.angle), sin(self.cur_state_.angle)]
        x = np.sum(vec * multipliers)

        multipliers = [-sin(self.cur_state_.angle), cos(self.cur_state_.angle)]
        y = np.sum(vec * multipliers)

        if x >= 0:
            return RIGHT_ACTION if x >= y else UP_ACTION
        else:
            return LEFT_ACTION if -x >= y else UP_ACTION

    @property
    def priority(self):
        if self.cur_state_ is None or self.prev_state_ is None:
            return 0

        vy = self.cur_state_.velocity[1]
        return self.config.max_priority if abs(vy) > self.config.max_y_velocity else 0
