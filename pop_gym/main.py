import gym

from balancer.DefaultBalancer import DefaultBalancer
from controller.LandingController import LandingController, LandingControllerConfig as LandConf
from controller.VelocityController import VelocityController, VelocityControllerConfig as VelConf
from others.State import to_state

if __name__ == '__main__':
    episodes_amount = 1
    steps_amount = 1000
    env = gym.make('LunarLander-v2')
    balancer = DefaultBalancer([
        VelocityController(VelConf(max_y_velocity=0.4, max_priority=0.8)),
        LandingController(LandConf(min_y_pos=0.3, max_priority=1, max_y_velocity=0.2)),
    ])

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
