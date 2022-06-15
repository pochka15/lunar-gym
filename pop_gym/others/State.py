from dataclasses import dataclass
import numpy as np

IDLE_ACTION = 0
LEFT_ACTION = 1
UP_ACTION = 2
RIGHT_ACTION = 3


# noinspection PyShadowingNames
def to_state(observation):
    return State(
        position=np.array([observation[0], observation[1]]),
        velocity=np.array([observation[2], observation[3]]),
        angle=observation[4],
        angular_velocity=observation[5],
        is_left_on_the_ground=observation[6],
        is_right_on_the_ground=observation[7])


def format_float(value):
    return "{:.2f}".format(value)


@dataclass
class State:
    position: np.ndarray
    velocity: np.ndarray
    angle: float
    angular_velocity: np.ndarray
    is_left_on_the_ground: bool
    is_right_on_the_ground: bool

    def __str__(self) -> str:
        return f"Position: x: {format_float(self.position[0])}, y: {format_float(self.position[1])}\n" \
               f"Velocity: x: {format_float(self.velocity[0])}, y: {format_float(self.velocity[1])}\n" \
               f"Angle: {format_float(self.angle)}\n" \
               f"Angular velocity: {format_float(self.angle)}\n" \
               f"Left leg is on the ground: {'Yes' if self.is_left_on_the_ground else 'No'}\n" \
               f"Right leg is on the ground: {'Yes' if self.is_right_on_the_ground else 'No'}"
