
import math, json, time, numpy as np
from binary_quantizer import Quantizer
from fuzzy_extractor import SampleLock


_1024 = np.genfromtxt('1024.csv', delimiter = ',')

loop_bound = math.floor(math.exp(0.2 * 80))
extractor = SampleLock(loop_bound)


def read_user_templates() -> dict:

    return json.load(open('user_templates.json', 'r'))


def reliable_index(data: np.ndarray):

    result = []
    m = len(data)

    for i in range(1024):
        mean = data[:, i].mean()
        diff = data[:, i] - mean
        sqrs = (diff ** 2).sum()
        rval = (0 - sqrs) / (m - 1)
        result += [rval]

    return np.argsort(result)[512:]


def reliable_bits(arr: np.ndarray, index: list):
    
    quantizer = Quantizer()
    mean = arr.mean(axis = 0)
    return quantizer.sign(mean[index])


def key_generate(idx_template: list):

    entry = _1024[idx_template[:5]]
    index = reliable_index(entry)
    entry = reliable_bits(entry, index)
    key_0 = extractor.generate(entry)
    return key_0, index


def key_reproduce(idx_template: list, index: list):

    entry = _1024[idx_template[5:8]]
    entry = reliable_bits(entry, index)
    return extractor.reproduce(entry)


def main():

    user = read_user_templates()

    user_31 = user['31']
    user_34 = user['34']

    start = time.time()
    key, index = key_generate(user_31)
    print(key)
    print(time.time() - start)

    start = time.time()    
    key = key_reproduce(user_31, index)
    print(key)
    print(time.time() - start)



main()
