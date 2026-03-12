def compute_reward(delivery_time, driver_idle):

    reward = 0

    reward -= delivery_time * 0.1

    reward -= driver_idle * 0.05

    return reward