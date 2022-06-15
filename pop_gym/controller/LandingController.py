from typing import Optional
from dataclasses import dataclass
from controller.Controller import Controller
from others.State import UP_ACTION, State


@dataclass
class LandingControllerConfig:
    max_priority: float
    max_y_velocity: float


class LandingController(Controller):
    """
    It tries slow down the lunar when lunar is close to y coord = 0.
    If lunar has low velocity then this controller gives priority = 0
    """

    def __init__(self, config: LandingControllerConfig):
        self.cur_state_: Optional[State] = None
        self.config = config

    def handle_state(self, state: State):
        self.cur_state_ = state

    @property
    def action(self):
        return UP_ACTION

    @property
    def priority(self):
        if self.cur_state_ is None:
            return 0

        y = self.cur_state_.position[1]
        y_velocity = self.cur_state_.velocity[1]

        # hardcoded
        y_bound = 0.2
        if y < y_bound and abs(y_velocity) > self.config.max_y_velocity:
            return self.config.max_priority
        else:
            return 0
