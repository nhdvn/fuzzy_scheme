
import json
import numpy as np

udata = np.genfromtxt('../data/Timit', delimiter=',')


def distance(x, y):  # normalized hamming distance

    count = 0

    for xbit, ybit in zip(x, y):
        if xbit != ybit:
            count += 1

    return count / len(x)


def save_error(intra, inter, filename: str):

    obj = {'intra': intra, 'inter': inter}

    with open(filename, 'w') as outfile:

        json.dump(obj, outfile, indent=4)


def enumerate_users() -> dict:

    result = {}

    for row, data in enumerate(udata):

        user = int(data[-1])

        if user not in result:
            result[user] = []

        result[user] += [row]

    return result


def reliable_index(data: np.ndarray):

    result = []

    for i in range(512):
        mean = data[:, i].mean()
        diff = data[:, i] - mean
        sqrs = (diff ** 2).sum()
        result.append(sqrs)

    return np.argsort(result)[:256]


def reliable_bits(arr: np.ndarray, index: list):

    res = ''
    mean = arr.mean(axis=0)

    for val in mean[index]:
        res += '0' if val <= 0 else '1'

    return res
