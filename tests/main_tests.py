import gym
import csv

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.SamePositionController import SamePositionController
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

    normal_heights = [0.3, 0.35, 0.4, 0.45, 0.5]
    low_heights = [0.1, 0.15, 0.2, 0.25]
    high_accelerations = [7, 9, 11, 13]
    max_x_distances = [0.2, 0.25, 0.3, 0.35, 0.4]
    frequencies = [2, 4, 6, 8]

    i = 1
    for normal in normal_heights:
        vel_conf.normal_height = normal

        for low in low_heights:
            vel_conf.low_height = low

            for high in high_accelerations:
                vel_conf.high_acceleration = high

                for distance in max_x_distances:
                    pos_conf.max_x_distance = distance

                    for freq in frequencies:
                        freq_conf.frequency = freq
                        simulate_and_store_results(f'{str(vel_conf.max_y_velocity)}_{str(i)}', balancer, freq_conf, log,
                                                   pos_conf, vel_conf)
                        i += 1


def simulate_and_store_results(prefix, balancer, freq_conf, log, pos_conf, vel_conf):
    results = simulate(balancer, log, 30)
    with open('results/' + prefix + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Done', 'Reward', 'Steps'])
        for result in results:
            writer.writerow(result)
    with open('configs/' + prefix + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['vel_conf.max_y_velocity', 'vel_conf.normal_height',
                         'vel_conf.low_height', 'vel_conf.safe_angle', 'vel_conf.max_priority',
                         'vel_conf.high_acceleration',
                         'pos_conf.max_x_distance', 'pos_conf.max_priority',
                         'freq_conf.frequency'])
        writer.writerow([vel_conf.max_y_velocity, vel_conf.normal_height,
                         vel_conf.low_height, vel_conf.safe_angle, vel_conf.max_priority,
                         vel_conf.high_acceleration,
                         pos_conf.max_x_distance, pos_conf.max_priority,
                         freq_conf.frequency])
