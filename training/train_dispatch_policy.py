import torch
import torch.nn as nn
import torch.optim as optim

from digital_twin.rl_env import LogisticsEnv


class PolicyNet(nn.Module):

    def __init__(self):

        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(10, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            nn.Linear(64, 50)

        )

    def forward(self, x):

        return self.net(x)


env = LogisticsEnv()

model = PolicyNet()

optimizer = optim.Adam(model.parameters(), lr=0.001)


for episode in range(100):

    state = env.reset()

    total_reward = 0

    for step in range(24):

        state_tensor = torch.tensor(state).float()

        logits = model(state_tensor)

        probs = torch.softmax(logits, dim=0)

        action = torch.multinomial(probs, 1).item()

        next_state, reward, done, _ = env.step(action)

        log_prob = torch.log(probs[action] + 1e-8)

        loss = -log_prob * reward

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        state = next_state

        total_reward += reward

    print("Episode:", episode, "Reward:", total_reward)

torch.save(model.state_dict(), "models/digital_twin_dispatch.pt")