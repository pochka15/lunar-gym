from controller.Controller import Controller
from others.State import State, UP_ACTION


class SamePositionController(Controller):
    """
    It's an ugly controller that tries to lift lunar up in case position is not different
    from given N states before
    """

    def __init__(self):
        self.required_cached_states_amount = 40
        self.cached_states = []

    @property
    def action(self):
        return UP_ACTION

    @property
    def priority(self):
        if len(self.cached_states) < self.required_cached_states_amount:
            return 0

        lhs = self.cached_states[-1].position
        rhs = self.cached_states[-self.required_cached_states_amount].position
        if abs(abs(lhs[0]) - abs(rhs[0])) < 0.001 or abs(abs(lhs[1]) - abs(rhs[1])) < 0.001:
            return 1
        return 0

    def handle_state(self, state: State):
        self.cached_states.append(state)
        if len(self.cached_states) > 2 * self.required_cached_states_amount:
            self.cached_states.clear()
