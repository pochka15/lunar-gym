from dataclasses import dataclass
from typing import Optional

from controller.Controller import Controller
from others.State import State, LEFT_ACTION, RIGHT_ACTION


@dataclass
class PositionControllerConfig:
    max_x_distance: float
    max_priority: float


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
        if distance > self.config.max_x_distance or self.state.position[1] < min_position:
            return self.config.max_priority
        return 0

    def handle_state(self, state: State):
        self.state = state
