import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.FrequencyController import FrequencyController, FrequencyControllerConfig as FreqConfig
from controller.LandingController import LandingController, LandingControllerConfig as LandConf
from controller.PositionController import PositionController, PositionControllerConfig as PosConf
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state

if __name__ == '__main__':
    episodes_amount = 1
    steps_amount = 500
    env = gym.make('LunarLander-v2')
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
