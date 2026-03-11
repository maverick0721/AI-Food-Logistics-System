import yaml
from pathlib import Path


def load_config(path):

    path = Path(path)

    with open(path) as f:
        config = yaml.safe_load(f)

    return config