import torch


class BaseModel(torch.nn.Module):

    def save(self, path):

        torch.save(self.state_dict(), path)

    def load(self, path):

        self.load_state_dict(torch.load(path))