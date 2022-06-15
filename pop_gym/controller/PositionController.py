from typing import Optional

from controller.Controller import Controller
from others.State import UP_ACTION, State


class PositionController(Controller):
    def __init__(self):
        self.cur_state_: Optional[State] = None
        self.counter = 0

    def handle_state(self, state: State):
        self.cur_state_ = state
        self.counter += 1

    @property
    def action(self):
        return UP_ACTION

    @property
    def priority(self):
        if self.cur_state_ is None:
            return 0

        y = self.cur_state_.position[1]
        magic_bound = 0.2
        if self.counter > 2:
            self.counter = 0

            return 1 if y < magic_bound else 0
        return 0
