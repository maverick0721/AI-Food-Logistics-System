import torch
import torch.optim as optim

from digital_twin.rl_env import LogisticsEnv
from training.policy_model import PolicyNet


def main():
    env = LogisticsEnv()
    model = PolicyNet()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for episode in range(100):
        state = env.reset()
        total_reward = 0

        for _ in range(24):
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

            if done:
                break

        print("Episode:", episode, "Reward:", total_reward)

    torch.save(model.state_dict(), "models/digital_twin_dispatch.pt")


if __name__ == "__main__":
    main()