import csv

from os import listdir
from os.path import isfile, join
from controller.FrequencyController import FrequencyControllerConfig
from controller.PositionController import PositionControllerConfig
from controller.VelocityController import VelocityControllerConfig
import matplotlib.pyplot as plt

RESULTS_DIR_NAME = 'results'
CONFIGS_DIR_NAME = 'configs'


def get_result_files(prefix=None):
    return [f for f in listdir(RESULTS_DIR_NAME)
            if (isfile(join(RESULTS_DIR_NAME, f)) and
                (prefix is None or
                 (prefix is not None and f.startswith(prefix))))]


def count_wins(file_name):
    with open(f'{RESULTS_DIR_NAME}/{file_name}') as csvfile:
        reader = csv.reader(csvfile)
        result = 0

        # Read header
        _ = next(reader)

        for row in reader:
            reward = row[1]
            if float(reward) >= 200:
                result += 1
        return result


def get_configs(file_name):
    with open(f'{CONFIGS_DIR_NAME}/{file_name}') as csvfile:
        reader = csv.reader(csvfile)

        # Read header
        _ = next(reader)

        row = list(float(x) for x in next(reader))
        [  # velocity
            max_y_velocity, normal_height,
            low_height, safe_angle, velocity_max_priority,
            high_acceleration,

            # pos
            max_x_distance, pos_max_priority,

            # freq
            frequency
        ] = row
        vel_conf = VelocityControllerConfig(
            max_y_velocity=max_y_velocity, normal_height=normal_height,
            low_height=low_height, safe_angle=safe_angle,
            max_priority=velocity_max_priority,
            high_acceleration=high_acceleration)
        pos_conf = PositionControllerConfig(max_x_distance=max_x_distance, max_priority=pos_max_priority)
        return vel_conf, pos_conf, FrequencyControllerConfig(frequency=frequency)


def group_files_by_wins(files):
    out = {}
    for f in files:
        amount = count_wins(f)
        out.setdefault(amount, []).append(f)
    return out


def get_values_frequency(values):
    """ Get dict containing value to amount of occurrences """
    out = {}
    for x in values:
        cur = out.setdefault(x, 0)
        out[x] = cur + 1
    return out


def format_configs(velocity_config: VelocityControllerConfig,
                   position_config: PositionControllerConfig,
                   frequency_config: FrequencyControllerConfig):
    return f"""
    velocity
        - max_y_velocity: {velocity_config.max_y_velocity}
        - normal_height: {velocity_config.normal_height}
        - low_height: {velocity_config.low_height} 
        - safe_angle: {velocity_config.safe_angle} 
        - max_priority: {velocity_config.max_priority} 
        - high_acceleration: {velocity_config.high_acceleration}

    position
        - max_x_distance: {position_config.max_x_distance}
        - max_priority: {position_config.max_priority}

    frequency
        - frequency: {frequency_config.frequency}"""


def store_results(results, prefix):
    with open('results/' + prefix + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Done', 'Wins', 'Steps'])
        for result in results:
            writer.writerow(result)


def store_configs(freq_conf, pos_conf, vel_conf, prefix):
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


def stem_plot(x, y):
    fig, ax = plt.subplots()
    ax.stem(x, y)
    plt.xticks(x)
    plt.show()
