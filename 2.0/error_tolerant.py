
from operator import *
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 5 # number of entry
k = 3 # number of valid


def mean_error_rate():

    user = enumerate_users()

    intra = []
    inter = []

    for ix, arr in user.items():
        
        size = len(arr)
        if n > size: continue
        
        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)

        for i in range(n, size, k):
            if i + k > size: break
            input = udata[arr[i: i + k]]
            input = reliable_bits(input, index)
            intra += [distance(input, entry)]

        for iv, brr in user.items():

            size = len(brr)
            if ix == iv: continue

            for i in range(0, size, k):
                if i + k > size: break
                input = udata[brr[i: i + k]]
                input = reliable_bits(input, index)
                inter += [distance(input, entry)]

    return intra, inter


def generate_key(row: list, start: int):

    entry = udata[row[:start]]
    index = reliable_index(entry)
    entry = reliable_bits(entry, index)
    value = extractor.generate(entry)
    return value, index 


def reproduce_key(row: list, index: list, start: int, step: int):

    entry = udata[row[start: start + step]]
    entry = reliable_bits(entry, index)
    return extractor.reproduce(entry)


def false_rate(key: bytes, row: list, idx: list, relate):

    rlen = len(row)
    rate = 0

    for i in range(n, rlen, k):
        if i + k > rlen: break
        if relate(key, reproduce_key(row, idx, i, k)):
            rate += 1

    return rate


def mean_false_rate():

    user = enumerate_users()
    accept = reject = 0

    for rate in [0.20, 0.25, 0.30]:

        global extractor
        extractor = SampleLock(rate, 512)

        for ix, arr in user.items():

            if n > len(arr): continue
            key, idx = generate_key(arr, n)
            reject += false_rate(key, arr, idx, ne)

            for iv, brr in user.items():
                if ix == iv: continue
                accept += false_rate(key, brr, idx, eq)
    
    return reject, accept


def main():

    jdata = '../json/error_0512.json'
    ifile = '../plot/plot_0512.png'

    intra, inter = mean_error_rate()
    
    save_error(intra, inter, jdata)
    visualize(jdata, ifile)
