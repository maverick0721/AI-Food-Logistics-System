from pathlib import Path
from utils.config import load_config

ROOT = Path(__file__).resolve().parent.parent


def test_config():

    cfg = load_config(ROOT / "configs/settings.yaml")

    assert "city" in cfg