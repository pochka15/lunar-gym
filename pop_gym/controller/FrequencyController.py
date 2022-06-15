from dataclasses import dataclass
from controller.Controller import Controller
from others.State import State, IDLE_ACTION


@dataclass
class FrequencyControllerConfig:
    frequency: float = 1

    def __str__(self):
        return f"""
FrequencyControllerConfig
  - frequency: {self.frequency}"""


class FrequencyController(Controller):
    """
    This is a wrapper for child controller.
    It allows to control how frequently given child controller should act.
    e.x. when we set::

        controller = FrequencyController(ChildController(), FrequencyControllerConfig(frequency=2))

    then this means that child controller will act each two frames in other frames
    controller variable gives an IDLE action

    You can set frequency = 3 then child controller will act ech three frames and so on

    In the configuration frequency = 1 by default which means child controller can act each frame
    """

    @property
    def action(self):
        return self.child.action if self.can_act else IDLE_ACTION

    @property
    def priority(self):
        return self.child.priority if self.can_act else 0

    @property
    def can_act(self):
        return self.counter == self.config.frequency

    def handle_state(self, state: State):
        self.counter += 1
        if self.counter > self.config.frequency:
            self.counter = 1
        if self.can_act:
            self.child.handle_state(state)

    def __init__(self, child: Controller, config: FrequencyControllerConfig):
        self.counter = 0
        self.config = config
        self.child = child
