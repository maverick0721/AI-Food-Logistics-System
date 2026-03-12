import numpy as np


class StateEncoder:

    def encode(self, drivers, orders):

        state = []

        state.append(len(drivers))

        state.append(len(orders))

        state.append(np.random.rand())

        state.append(np.random.rand())

        while len(state) < 10:

            state.append(0)

        return np.array(state)