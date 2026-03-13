import ray
from ray.rllib.algorithms.ppo import PPOConfig

from rl_dispatch.multi_agent_env import FleetEnvironment


def main():
    ray.init(ignore_reinit_error=True)

    config = (
        PPOConfig()
        .environment(FleetEnvironment)
        .env_runners(num_env_runners=2)
        .training(train_batch_size=4000)
    )

    algo = config.build()
    for i in range(20):
        result = algo.train()
        print("Iteration:", i, "Reward:", result.get("episode_reward_mean"))


if __name__ == "__main__":
    main()