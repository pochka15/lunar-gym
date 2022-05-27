from functools import reduce

from State import State, IDLE_ACTION


class Balancer:
    def __init__(self, controllers):
        self.controllers_ = controllers

    def handle_state(self, state: State):
        for controller in self.controllers_:
            controller.handle_state(state)

    @property
    def action(self):
        best = reduce(lambda x, y: y if x.priority < y.priority else x, self.controllers_)
        return IDLE_ACTION if best.priority == 0 else best.action
