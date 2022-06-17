from controller.Controller import Controller
from others.State import State, UP_ACTION


class SamePositionController(Controller):
    """
    It's an ugly controller that tries to lift lunar up in case position is not different
    from given N states before
    """

    def __init__(self, log):
        self.log = log
        self.required_cached_states_amount = 40
        self.is_lifting = False
        self.lift_counter = 0
        self.lifts_amount = 10

    @property
    def action(self):
        return UP_ACTION

    @property
    def priority(self):
        if self.is_lifting:
            return 2
        return 0

    def handle_state(self, state: State):
        if len(self.log) < self.required_cached_states_amount:
            return

        if self.is_lifting:
            self.lift_counter += 1
            if self.lift_counter >= self.lifts_amount:
                self.is_lifting = False

        else:
            lhs = abs(self.log[-1].position)
            rhs = abs(self.log[-self.required_cached_states_amount].position)
            diff = abs(lhs - rhs)
            if diff[0] < 0.001 and diff[1] < 0.001:
                self.lift_counter = 0
                self.is_lifting = True
