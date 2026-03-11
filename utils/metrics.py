import numpy as np


def mae(pred, true):

    pred = np.array(pred)
    true = np.array(true)

    return np.mean(np.abs(pred - true))


def mse(pred, true):

    pred = np.array(pred)
    true = np.array(true)

    return np.mean((pred - true) ** 2)