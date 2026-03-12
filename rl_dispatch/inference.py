import torch

from rl_dispatch.agent import DispatchAgent


def load_agent():

    model = DispatchAgent(10, 20)

    model.load_state_dict(torch.load("models/dispatch_agent.pt"))

    model.eval()

    return model


def predict(state):

    model = load_agent()

    x = torch.tensor(state).float()

    logits = model(x)

    action = torch.argmax(logits).item()

    return action