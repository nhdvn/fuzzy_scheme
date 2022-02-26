
import math, json, numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk
from binary_quantizer import Quantizer
from fuzzy_extractor import SampleLock


_1024 = np.genfromtxt('1024.csv', delimiter = ',')
quantized = []
quantizer = Quantizer()


bits = 512
name = '{:04d}'.format(bits)


def read_user_templates() -> dict:

    json_file = open('user_templates.json', 'r')

    user_data = json.load(json_file)

    json_file.close()

    return user_data


def load_threshold_error():

    json_file = open(f'threshold_{name}.json', 'r')

    distance = json.load(json_file)

    json_file.close()

    return distance['intra'], distance['inter']


def distance(x, y): # hamming distance
    
    count = 0
    
    for xbit, ybit in zip(x, y):
        if xbit != ybit: count = count + 1
    
    return count / bits


def intra_distance(arr):

    ans = []
    n = len(arr)

    for u in range(0, n):
        for v in range(u + 1, n):
            x = quantized[arr[u]]
            y = quantized[arr[v]]
            ans += [distance(x, y)]

    return ans


def inter_distance(arr, brr):

    ans = []

    for u in arr:
        for v in brr:
            x = quantized[u] 
            y = quantized[v]
            ans += [distance(x, y)]

    return ans


def quantize_data():

    global quantized

    for row in _1024:
        res = quantizer.sign(row[:-1])
        quantized += [res]


def count_distance():

    quantize_data()

    user = read_user_templates()

    intra = []
    inter = []
    finis = []

    for i in user:
        intra += intra_distance(user[i])
        finis += [i]
        for j in user:
            if j in finis: continue
            inter += inter_distance(user[i], user[j])

    write_distance(intra, inter)


def write_distance(intra, inter):
    
    result = {}
    result['intra'] = intra
    result['inter'] = inter

    json_file = open(f'threshold_{name}.json', 'w')

    json.dump(result, json_file, indent = 4)

    json_file.close()


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
    
    mean = arr.mean(axis = 0)
    
    return quantizer.sign(mean[index])


def multi_count_distance():

    user = read_user_templates()

    n_entry = 5
    n_valid = 3

    intra = []
    inter = []

    for ix, arr in user.items():
        if n_entry > len(arr): continue
        entry = _1024[arr[:n_entry]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)

        for i in range(n_entry, len(arr), n_valid):
            if i + n_valid > len(arr): break
            input = _1024[arr[i: i + n_valid]]
            input = reliable_bits(input, index)
            intra += [distance(input, entry)]

        for iy, brr in user.items():
            if ix == iy: continue
            for i in range(0, len(brr), n_valid):
                if i + n_valid > len(brr): break
                input = _1024[brr[i: i + n_valid]]
                input = reliable_bits(input, index)
                inter += [distance(input, entry)]

    write_distance(intra, inter)


def multi_error_rate():

    user = read_user_templates()

    n_entry = 5
    n_valid = 3

    false_accept = 0
    false_reject = 0

    for rate in [0.20, 0.25, 0.30]:

        loop_bound = math.ceil(math.exp(rate * 80))
        extractor = SampleLock(loop_bound)

        for ix, arr in user.items():

            if ix != '31': continue
            print(f'attempt user {ix}')

            if n_entry > len(arr): continue
            entry = _1024[arr[:n_entry]]
            index = reliable_index(entry)
            entry = reliable_bits(entry, index)
            key_0 = extractor.generate(entry)
            
            for i in range(n_entry, len(arr), n_valid):
                if i + n_valid > len(arr): break
                intra = _1024[arr[i: i + n_valid]]
                intra = reliable_bits(intra, index)
                key_1 = extractor.reproduce(intra)
                if key_0 != key_1: false_accept += 1

            print(f'intra error: {false_accept}')
            
            for iy, brr in user.items():
                if ix == iy: continue
                for i in range(0, len(brr), n_valid):
                    if i + n_valid > len(brr): break
                    inter = _1024[brr[i: i + n_valid]]
                    inter = reliable_bits(inter, index)
                    key_2 = extractor.reproduce(inter)
                    if key_0 == key_2: false_reject += 1
                
                print(f'inter error with user {iy}: {false_reject}')
    
        print(f'threshold {rate}: {false_accept} {false_reject}')


def visualize():

    intra_list, inter_list = load_threshold_error()

    intra_weights = np.ones(len(intra_list)) / len(intra_list)
    inter_weights = np.ones(len(inter_list)) / len(inter_list)

    plt.hist(intra_list, bins = 10, weights = intra_weights, rwidth = 0.7, alpha = 0.7)
    plt.hist(inter_list, bins = 20, weights = inter_weights, rwidth = 0.7, alpha = 0.7)
    plt.xticks([0.25, 0.5, 0.75])
    plt.legend(['Intra', 'Inter'])

    plt.gca().yaxis.set_major_formatter(mtk.PercentFormatter(1))
    plt.savefig(f'histogram_{name}.png')


multi_count_distance()
visualize()