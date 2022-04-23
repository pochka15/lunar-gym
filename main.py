from dataclasses import dataclass

import gym

IDLE_ACTION = 0
LEFT_ACTION = 1
UP_ACTION = 2
RIGHT_ACTION = 3


def create_dumb_action(x, current_step):
    if current_step % 4 == 0:
        return UP_ACTION
    if current_step % 2 == 0:
        return IDLE_ACTION
    return LEFT_ACTION if x >= 0 else RIGHT_ACTION


@dataclass
class Coords2D:
    x: float
    y: float


def format_float(value):
    return "{:.2f}".format(value)


@dataclass
class State:
    position: Coords2D
    velocity: Coords2D
    angle: float
    angular_velocity: Coords2D
    is_left_on_the_ground: bool
    is_right_on_the_ground: bool

    def __str__(self) -> str:
        return f"Position: x: {format_float(self.position.x)}, y: {format_float(self.position.y)}\n" \
               f"Velocity: x: {format_float(self.velocity.x)}, y: {format_float(self.velocity.y)}\n" \
               f"Angle: {format_float(self.angle)}\n" \
               f"Angular velocity: {format_float(self.angle)}\n" \
               f"Left leg is on the ground: {'Yes' if self.is_left_on_the_ground else 'No'}\n" \
               f"Right leg is on the ground: {'Yes' if self.is_right_on_the_ground else 'No'}"


# noinspection PyShadowingNames
def to_state(observation):
    return State(
        position=Coords2D(observation[0], observation[1]),
        velocity=Coords2D(observation[1], observation[2]),
        angle=observation[3],
        angular_velocity=Coords2D(observation[4], observation[5]),
        is_left_on_the_ground=observation[6],
        is_right_on_the_ground=observation[7])


if __name__ == '__main__':
    # Configurations
    episodes_amount = 1
    steps_amount = 100

    env = gym.make('LunarLander')
    for i_episode in range(episodes_amount):
        # noinspection PyRedeclaration
        observation = env.reset()
        for t in range(steps_amount):
            env.render()

            action = create_dumb_action(observation[0], t)
            observation, reward, done, info = env.step(action)
            state = to_state(observation)

            print(f"Reward: {format_float(reward)}\n{state}")

            if done:
                print("Episode finished after {} steps".format(t + 1))
                break
    env.close()
