from math import cos, sin

import numpy as np
from typing import Optional

from State import State, LEFT_ACTION, RIGHT_ACTION, UP_ACTION, IDLE_ACTION


class VelocityController:
    def __init__(self):
        self.prev_state_: Optional[State] = None
        self.cur_state_: Optional[State] = None

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

        magic_bound = 0.2
        vy = self.cur_state_.velocity
        return 1 if abs(vy) > magic_bound else 0
