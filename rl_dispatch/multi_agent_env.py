import gym
import numpy as np


class FleetEnvironment(gym.Env):

    def __init__(self, drivers=50, orders=20):

        self.drivers = drivers
        self.orders = orders

        self.state_size = 20

    def reset(self):

        self.state = np.random.rand(self.state_size)

        return self.state

    def step(self, actions):

        reward = -np.sum(actions) * 0.01

        next_state = np.random.rand(self.state_size)

        done = False

        return next_state, reward, done, {}