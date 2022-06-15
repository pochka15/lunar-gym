from functools import reduce

from balancer.Balancer import Balancer
from controller.Controller import Controller
from others.State import IDLE_ACTION, State


class DefaultBalancer(Balancer):
    def __init__(self, controllers: [Controller]):
        self.controllers_ = controllers

    def make_action(self, state: State):
        for controller in self.controllers_:
            controller.handle_state(state)

        best: Controller = reduce(lambda prev, cur: cur if prev.priority < cur.priority else prev, self.controllers_)
        return IDLE_ACTION if best.priority == 0 else best.action
