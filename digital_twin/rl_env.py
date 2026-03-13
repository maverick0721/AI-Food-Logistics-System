import gym
import numpy as np

from digital_twin.simulator import DigitalTwinSimulator


class LogisticsEnv(gym.Env):

    def __init__(self):

        self.sim = DigitalTwinSimulator()

        self.state_size = 10
        self.action_space = gym.spaces.Discrete(50)

        self.observation_space = gym.spaces.Box(
            low=0,
            high=1,
            shape=(self.state_size,)
        )

    def reset(self):

        self.hour = 0

        return np.random.rand(self.state_size)

    def step(self, action):

        self.hour += 1

        self.sim.step(self.hour)

        reward = np.random.rand()

        next_state = np.random.rand(self.state_size)

        done = self.hour >= 24

        return next_state, reward, done, {}