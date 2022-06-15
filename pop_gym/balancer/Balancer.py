import abc

from others.State import State


class Balancer(abc.ABC):
    @abc.abstractmethod
    def make_action(self, state: State):
        pass
