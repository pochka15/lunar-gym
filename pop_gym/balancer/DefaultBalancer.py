from functools import reduce

from balancer.Balancer import Balancer
from others.State import IDLE_ACTION, State


class DefaultBalancer(Balancer):
    def __init__(self, controllers):
        self.controllers_ = controllers

    def make_action(self, state: State):
        for controller in self.controllers_:
            controller.handle_state(state)

        best = reduce(lambda x, y: y if x.priority < y.priority else x, self.controllers_)
        return IDLE_ACTION if best.priority == 0 else best.action
