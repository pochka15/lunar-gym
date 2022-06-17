from time import sleep

import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.SamePositionController import SamePositionController
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state

if __name__ == '__main__':
    episodes_amount = 3
    steps_amount = 500
    env = gym.make('LunarLander-v2')
    vel_conf = VelConf(max_y_velocity=0.4, normal_height=0.4, low_height=0.15, safe_angle=10, high_acceleration=9,
                       max_priority=2)
    pos_conf = PosConf(max_x_distance=0.4, max_priority=1)
    freq_conf = FreqConfig(frequency=4)
    log = []
    balancer = DefaultBalancer([
        SamePositionController(log),
        FrequencyController(PositionController(pos_conf), freq_conf),
        VelocityController(vel_conf, log),
    ], is_debug=False)

    for i_episode in range(episodes_amount):
        # noinspection PyRedeclaration
        observation = env.reset()
        log.clear()
        for t in range(steps_amount):
            env.render()

            state = to_state(observation)

            log.append(state)
            observation, reward, done, info = env.step(balancer.make_action(state))

            if done:
                print("Episode finished after {} steps, reward {}".format(t + 1, reward))
                break
    env.close()
