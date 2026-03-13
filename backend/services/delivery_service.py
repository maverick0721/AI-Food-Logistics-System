import torch

from training.policy_model import PolicyNet


model = PolicyNet()

model.load_state_dict(
    torch.load("models/digital_twin_dispatch.pt")
)

model.eval()


def assign_driver(state):

    x = torch.tensor(state).float()

    logits = model(x)

    action = torch.argmax(logits).item()

    return action