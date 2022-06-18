import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.SamePositionController import SamePositionController
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state
from test_utils import get_reward, get_configs, get_result_files, stem_plot, group_files_by_reward, \
    get_values_frequency, store_results, store_configs


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


def test_plot_velocities():
    reward_to_files = group_files_by_reward(get_result_files())
    reward = 18
    files = reward_to_files[reward]
    values = list(get_configs(file)[0].max_y_velocity for file in files)
    statistics = get_values_frequency(values)
    stem_plot(list(statistics.keys()), list(statistics.values()))


def test_plot_max_x_distance():
    reward_to_files = group_files_by_reward(get_result_files())
    reward = 16
    files = reward_to_files[reward]
    values = list(get_configs(file)[1].max_x_distance for file in files)
    statistics = get_values_frequency(values)
    stem_plot(list(statistics.keys()), list(statistics.values()))


def test_very_long():
    vel_conf = VelConf(max_y_velocity=0.4, normal_height=0.4, low_height=0.15, safe_angle=10, high_acceleration=9,
                       max_priority=2)
    pos_conf = PosConf(max_x_distance=0.35, max_priority=1)
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
                        prefix = f'{str(vel_conf.max_y_velocity)}_{str(i)}'
                        results = simulate(balancer, log, 30)
                        store_results(results, prefix)
                        store_configs(freq_conf, pos_conf, vel_conf, prefix)
                        i += 1


def test_quick():
    vel_conf = VelConf(max_y_velocity=0.45, normal_height=0.4, low_height=0.1, safe_angle=10, high_acceleration=7,
                       max_priority=2)
    pos_conf = PosConf(max_x_distance=0.35, max_priority=1)
    freq_conf = FreqConfig(frequency=4)
    log = []
    balancer = DefaultBalancer([
        SamePositionController(log),
        FrequencyController(PositionController(pos_conf), freq_conf),
        VelocityController(vel_conf, log),
    ], is_debug=False)

    prefix = 'tmp'
    results = simulate(balancer, log, 30)
    store_results(results, prefix)
    store_configs(freq_conf, pos_conf, vel_conf, prefix)
    print(get_reward('tmp.csv'))
