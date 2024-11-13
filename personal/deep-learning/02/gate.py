import numpy as np


def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    bias = -0.7
    tmp = np.sum(w * x) + bias
    ret = 1 if tmp > 0 else 0

    return ret


def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    bias = 0.7
    tmp = np.sum(w * x) + bias
    ret = 1 if tmp > 0 else 0

    return ret


def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    bias = -0.4
    tmp = np.sum(w * x) + bias
    ret = 1 if tmp > 0 else 0

    return ret


def NOT(x1):
    return NAND(x1, x1)


def XOR(x1, x2):
    return AND(NAND(x1, x2), OR(x1, x2))


if __name__ == "__main__":
    for x in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        y1 = AND(x[0], x[1])
        y2 = NAND(x[0], x[1])
        y3 = OR(x[0], x[1])
        y4 = XOR(x[0], x[1])
        y5 = NOT(AND(x[0], x[1]))
        print(str(x) + "AND => " + str(y1))
        print(str(x) + "NAND => " + str(y2))
        print(str(x) + "OR => " + str(y3))
        print(str(x) + "XOR => " + str(y4))
        print(str(x) + "XOR => " + str(y4))
        print(str(x) + "NOT & AND => " + str(y5))
