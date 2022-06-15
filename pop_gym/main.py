import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.PositionController import PositionController
from controller.VelocityController import VelocityController
from others.State import to_state

if __name__ == '__main__':
    episodes_amount = 1
    steps_amount = 1000
    env = gym.make('LunarLander-v2')
    balancer = DefaultBalancer([VelocityController(), PositionController()])

    for i_episode in range(episodes_amount):
        # noinspection PyRedeclaration
        observation = env.reset()
        for t in range(steps_amount):
            env.render()

            state = to_state(observation)
            observation, reward, done, info = env.step(balancer.make_action(state))

            if done:
                print("Episode finished after {} steps, reward {}".format(t + 1, reward))
                break
    env.close()
