import os

import torch
import torch.distributions as dist
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

        state, _ = env.reset()

        total_reward = 0

        for step in range(50):

            state_tensor = torch.tensor(state).float()

            logits = model(state_tensor)

            distribution = dist.Categorical(logits=logits)
            action = distribution.sample()

            next_state, reward, done, truncated, _ = env.step(action.item())

            loss = -distribution.log_prob(action) * reward

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            state = next_state

            total_reward += reward

        print("Episode", episode, "Reward", total_reward)

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/dispatch_agent.pt")

    print("Model saved to models/dispatch_agent.pt")


if __name__ == "__main__":

    train()