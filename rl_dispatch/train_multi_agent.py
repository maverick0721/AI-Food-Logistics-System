import ray
from ray.rllib.algorithms.ppo import PPOConfig

from rl_dispatch.multi_agent_env import FleetEnvironment


ray.init()

config = (

    PPOConfig()

    .environment(FleetEnvironment)

    .rollouts(num_rollout_workers=2)

    .training(train_batch_size=4000)

)

algo = config.build()

for i in range(20):

    result = algo.train()

    print("Iteration:", i, "Reward:", result["episode_reward_mean"])