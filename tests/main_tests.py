import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.SamePositionController import SamePositionController
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state
from test_utils import count_wins, store_results, store_configs


def simulate(balancer, log, episodes_amount=1):
    steps_amount = 500
    env = gym.make('LunarLander-v2')
    result = []
    for i_episode in range(episodes_amount):
        observation = env.reset()
        t = 0
        is_done = False
        total_reward = 0
        log.clear()
        for t in range(steps_amount):
            state = to_state(observation)
            log.append(state)
            observation, reward, done, info = env.step(balancer.make_action(state))
            total_reward += reward
            if done:
                is_done = True
                break
        print(f"{i_episode + 1}: {total_reward}")
        result.append([is_done, total_reward, t + 1])
    env.close()
    return result


def test_very_long():
    vel_conf = VelConf(max_y_velocity=0.4, normal_height=0.4,
                       low_height=0.1, safe_angle=10,
                       high_acceleration=10, max_priority=2)
    pos_conf = PosConf(max_x_distance=0.4, max_priority=1)
    freq_conf = FreqConfig(frequency=4)
    log = []
    balancer = DefaultBalancer([
        SamePositionController(log),
        FrequencyController(PositionController(pos_conf), freq_conf),
        VelocityController(vel_conf, log),
    ], is_debug=False)

    normal_heights = [0.5] * 10
    low_heights = [0.1]
    high_accelerations = [10]
    max_x_distances = [0.4]
    frequencies = [4]

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
                        prefix = f'proper_final_{str(i)}'
                        results = simulate(balancer, log, 15)
                        store_results(results, prefix)
                        store_configs(freq_conf, pos_conf, vel_conf, prefix)
                        i += 1


def test_quick():
    vel_conf = VelConf(max_y_velocity=0.45, normal_height=0.4,
                       low_height=0.1, safe_angle=10,
                       high_acceleration=9, max_priority=2)
    pos_conf = PosConf(max_x_distance=0.4, max_priority=1)
    freq_conf = FreqConfig(frequency=4)
    log = []
    balancer = DefaultBalancer([
        SamePositionController(log),
        FrequencyController(PositionController(pos_conf), freq_conf),
        VelocityController(vel_conf, log),
    ], is_debug=False)

    prefix = 'tmp'
    results = simulate(balancer, log, 15)
    store_results(results, prefix)
    store_configs(freq_conf, pos_conf, vel_conf, prefix)
    print('Reward:', count_wins(f'{prefix}.csv'))
