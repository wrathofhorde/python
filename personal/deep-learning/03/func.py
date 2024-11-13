import numpy as np
import matplotlib.pylab as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def step(x):
    return np.array(x > 0, dtype=np.int32)


def identify(x):
    return x


def softmax(x):
    c = np.max(x)
    exp_x = np.exp(x - c)
    return exp_x / np.sum(exp_x)


if __name__ == "__main__":
    x = np.array([1, 2, 3])
    print(softmax(x))
