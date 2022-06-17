from dataclasses import dataclass
from typing import Optional

from controller.Controller import Controller
from others.State import State, LEFT_ACTION, RIGHT_ACTION


def are_opposite_signs(a, b):
    if a >= 0 and b >= 0:
        return False
    if a < 0 and b < 0:
        return False
    return True


@dataclass
class PositionControllerConfig:
    max_x_distance: float
    max_priority: float

    def __str__(self):
        return f"""
PositionControllerConfig
  - max_x_distance: {self.max_x_distance}
  - max_priority: {self.max_priority}"""


class PositionController(Controller):
    def __init__(self, config: PositionControllerConfig):
        self.state: Optional[State] = None
        self.config = config

    @property
    def action(self):
        if self.state.position[0] > 0:
            return LEFT_ACTION
        return RIGHT_ACTION

    @property
    def priority(self):
        distance = abs(self.state.position[0])
        # Hardcoded
        min_position = -0.05
        if not self.is_velocity_towards_center and (
                distance > self.config.max_x_distance or
                self.state.position[1] < min_position):
            return self.config.max_priority
        return 0

    @property
    def is_velocity_towards_center(self):
        return are_opposite_signs(self.state.position[0], self.state.velocity[0])

    def handle_state(self, state: State):
        self.state = state
