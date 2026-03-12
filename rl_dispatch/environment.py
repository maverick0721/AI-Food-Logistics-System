import gymnasium as gym
import numpy as np


class DispatchEnvironment(gym.Env):

    def __init__(self):

        self.num_drivers = 20
        self.num_orders = 10

        self.state_size = 10

        self.action_space = gym.spaces.Discrete(self.num_drivers)

        self.observation_space = gym.spaces.Box(
            low=0,
            high=1,
            shape=(self.state_size,)
        )

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        self.state = np.random.rand(self.state_size)

        return self.state, {}

    def step(self, action):

        reward = np.random.rand()

        done = False

        next_state = np.random.rand(self.state_size)

        return next_state, reward, done, False, {}