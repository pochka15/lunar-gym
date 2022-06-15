from functools import reduce

from balancer.Balancer import Balancer
from controller.Controller import Controller
from others.State import IDLE_ACTION, State


class DefaultBalancer(Balancer):
    def __init__(self, controllers: [Controller], is_debug=False):
        self.controllers_ = controllers
        self.is_debug = is_debug

    def make_action(self, state: State):
        for controller in self.controllers_:
            controller.handle_state(state)

        best: Controller = reduce(lambda prev, cur: cur if prev.priority < cur.priority else prev, self.controllers_)
        if best.priority != 0 and self.is_debug:
            print(type(best).__name__)
        return IDLE_ACTION if best.priority == 0 else best.action
