import abc

from others.State import State


class Controller(abc.ABC):
    @property
    @abc.abstractmethod
    def action(self):
        pass

    @property
    @abc.abstractmethod
    def priority(self):
        pass

    @abc.abstractmethod
    def handle_state(self, state: State):
        pass
