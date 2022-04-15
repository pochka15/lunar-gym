import gym

IDLE_ACTION = 0
LEFT_ACTION = 1
UP_ACTION = 2
RIGHT_ACTION = 3


def create_dumb_action(x, current_step):
    if current_step % 4 == 0:
        return UP_ACTION
    if current_step % 2 == 0:
        return IDLE_ACTION
    return LEFT_ACTION if x >= 0 else RIGHT_ACTION


if __name__ == '__main__':
    # Configurations
    episodes_amount = 1
    steps_amount = 100

    env = gym.make('LunarLander')
    for i_episode in range(episodes_amount):
        # noinspection PyRedeclaration
        observation = env.reset()
        for t in range(steps_amount):
            env.render()
            print(observation[0])
            action = create_dumb_action(observation[0], t)
            observation, reward, done, info = env.step(action)
            print(f"Reward: {str(reward)}")
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break
    env.close()
