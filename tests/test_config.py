from utils.config import load_config


def test_config():

    cfg = load_config("configs/settings.yaml")

    assert "city" in cfg