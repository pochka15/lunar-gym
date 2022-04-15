import gym

DO_NOTHING_ACTION = 0
FIRE_LEFT_ACTION = 1
FIRE_MAIN_ACTION = 2
FIRE_RIGHT_ACTION = 3

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
            print(observation)
            action = DO_NOTHING_ACTION
            observation, reward, done, info = env.step(action)
            print(f"Reward: {str(reward)}")
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break
    env.close()
