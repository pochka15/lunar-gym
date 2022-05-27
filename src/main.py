import gym

from Balancer import Balancer
from State import to_state
from VelocityController import VelocityController
from src.PositionController import PositionController

if __name__ == '__main__':
    episodes_amount = 10
    steps_amount = 1000
    env = gym.make('LunarLander')
    balancer = Balancer([VelocityController(), PositionController()])

    for i_episode in range(episodes_amount):
        # noinspection PyRedeclaration
        observation = env.reset()
        for t in range(steps_amount):
            env.render()

            state = to_state(observation)
            balancer.handle_state(state)
            observation, reward, done, info = env.step(balancer.action)

            if done:
                print("Episode finished after {} steps, reward {}".format(t + 1, reward))
                break
    env.close()
