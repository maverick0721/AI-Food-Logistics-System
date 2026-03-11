import wandb


def init_experiment(name):

    wandb.init(
        project="food-logistics-ai",
        name=name
    )