from pathlib import Path

try:
    import torch
    from training.policy_model import PolicyNet
except Exception:  # pragma: no cover - fallback for lightweight environments
    torch = None
    PolicyNet = None


def _resolve_model_path() -> Path | None:
    candidates = [
        Path("models/digital_twin_dispatch.pt"),
        Path("models/dispatch_agent.pt"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


model = None
if torch is not None and PolicyNet is not None:
    model = PolicyNet()
    model_path = _resolve_model_path()
    if model_path is not None:
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()


def _normalize_state(state):
    # Ensure inference input always matches the model's expected 10-feature vector.
    if torch is None:
        if isinstance(state, int):
            return [float(state)] + [0.0] * 9
        if isinstance(state, (list, tuple)):
            values = [float(v) for v in state[:10]]
            if len(values) < 10:
                values += [0.0] * (10 - len(values))
            return values
        return [0.0] * 10

    if isinstance(state, int):
        return torch.tensor([float(state)] + [0.0] * 9)

    x = torch.tensor(state).float().flatten()
    if x.numel() < 10:
        x = torch.cat([x, torch.zeros(10 - x.numel())])
    elif x.numel() > 10:
        x = x[:10]
    return x


def assign_driver(state):
    if torch is None or model is None:
        if isinstance(state, int):
            return state % 20
        return 0

    x = _normalize_state(state)
    with torch.no_grad():
        logits = model(x)
    return torch.argmax(logits).item()