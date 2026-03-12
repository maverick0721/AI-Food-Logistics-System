import torch
import numpy as np

from rl_dispatch.environment import DispatchEnvironment
from rl_dispatch.agent import DispatchAgent


def train():

    env = DispatchEnvironment()

    state_size = env.state_size
    action_size = env.num_drivers

    model = DispatchAgent(state_size, action_size)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for episode in range(100):

        state = env.reset()

        total_reward = 0

        for step in range(50):

            state_tensor = torch.tensor(state).float()

            logits = model(state_tensor)

            action = torch.argmax(logits).item()

            next_state, reward, done, _ = env.step(action)

            loss = -torch.tensor(reward)

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            state = next_state

            total_reward += reward

        print("Episode", episode, "Reward", total_reward)


if __name__ == "__main__":

    train()