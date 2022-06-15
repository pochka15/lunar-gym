import gym
import csv

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.LandingController import LandingController, LandingControllerConfig as LandConf
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.SamePositionController import SamePositionController
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state


def simulate(balancer, episodes_amount=1):
    steps_amount = 500
    env = gym.make('LunarLander-v2')
    reward = 0
    t = 0
    is_done = False
    result = []
    for i_episode in range(episodes_amount):

        # noinspection PyRedeclaration
        observation = env.reset()
        for t in range(steps_amount):
            env.render()
            state = to_state(observation)
            observation, reward, done, info = env.step(balancer.make_action(state))
            if done:
                is_done = True
                break
        print(f"Episode {i_episode}: {reward}")
        result.append([is_done, reward, t + 1])
    env.close()
    return result


def test_three_controllers():
    land_conf = LandConf(max_y_velocity=0.2, max_priority=1)
    vel_conf = VelConf(max_y_velocity=0.4, max_priority=1)
    pos_conf = PosConf(max_x_distance=0.4, max_priority=1)
    freq_conf = FreqConfig(frequency=3)
    balancer = DefaultBalancer([
        SamePositionController(),
        LandingController(land_conf),
        VelocityController(vel_conf),
        FrequencyController(PositionController(pos_conf),
                            freq_conf),
    ])
    results = simulate(balancer, 30)
    with open('results/result_4_same_velo_and_pos.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Done', 'Reward', 'Steps'])
        for result in results:
            writer.writerow(result)

    with open('results/config_4_same_velo_and_pos.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['land_conf.max_priority', 'land_conf.max_y_velocity',
                         'vel_conf.max_y_velocity', 'vel_conf.max_priority',
                         'pos_conf.max_x_distance', 'pos_conf.max_priority',
                         'freq_conf.frequency'])
        writer.writerow([land_conf.max_priority, land_conf.max_y_velocity,
                         vel_conf.max_y_velocity, vel_conf.max_priority,
                         pos_conf.max_x_distance, pos_conf.max_priority,
                         freq_conf.frequency])
