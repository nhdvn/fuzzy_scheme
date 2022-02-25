
import json, numpy as np

udata = np.genfromtxt('.gait_dataset', delimiter = ',')


def save_error(intra, inter):
    
    obj = {'intra': intra, 'inter': inter}

    with open(f'error.json', 'w') as outfile:

        json.dump(obj, outfile, indent = 4)


def enumerate_users() -> dict:

    result = {}

    for row, data in enumerate(udata):
        user = int(data[-1]) 
        if user in result:
            result[user] += [row]
        else:
            result[user] = []

    return result


def reliable_index(data: np.ndarray):

    result = []

    for i in range(1024):
        mean = data[:, i].mean()
        diff = data[:, i] - mean
        sqrs = (diff ** 2).sum()
        result.append(sqrs)

    return np.argsort(result)[:512]


def reliable_bits(arr: np.ndarray, index: list):
    
    res = ''
    mean = arr.mean(axis = 0)

    for each in mean[index]:
        if each > 0: res += '1'
        if each < 0: res += '0'
    
    return res