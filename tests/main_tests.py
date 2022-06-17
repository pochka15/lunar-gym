import gym
import csv

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.LandingController import LandingController, LandingControllerConfig as LandConf
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state


def simulate(balancer, log, episodes_amount=1):
    steps_amount = 500
    env = gym.make('LunarLander-v2')
    reward = 0
    t = 0
    is_done = False
    result = []
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
                is_done = True
                break
        print(f"{i_episode + 1}: {reward}")
        result.append([is_done, reward, t + 1])
    env.close()
    return result


def test_simulation():
    land_conf = LandConf(max_y_velocity=0.2, max_priority=1)
    vel_conf = VelConf(max_y_velocity=0.4, max_priority=2)
    pos_conf = PosConf(max_x_distance=0.3, max_priority=1)
    freq_conf = FreqConfig(frequency=3)
    log = []
    balancer = DefaultBalancer([
        LandingController(land_conf),
        VelocityController(vel_conf, log),
        FrequencyController(PositionController(pos_conf), freq_conf),
    ], is_debug=False)
    results = simulate(balancer, log, 30)
    with open('results/1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Done', 'Reward', 'Steps'])
        for result in results:
            writer.writerow(result)

    with open('configs/1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['land_conf.max_priority', 'land_conf.max_y_velocity',
                         'vel_conf.max_y_velocity', 'vel_conf.max_priority',
                         'pos_conf.max_x_distance', 'pos_conf.max_priority',
                         'freq_conf.frequency'])
        writer.writerow([land_conf.max_priority, land_conf.max_y_velocity,
                         vel_conf.max_y_velocity, vel_conf.max_priority,
                         pos_conf.max_x_distance, pos_conf.max_priority,
                         freq_conf.frequency])
