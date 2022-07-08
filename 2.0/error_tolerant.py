
from sys import argv

from numpy import ndarray
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 2  # number of entry
k = 1  # number of valid
l = 10
plot_name = '1_Timit_47000'


def mean_error_rate():

    users = enumerate_users()

    intra = []
    inter = []

    for ix, arr in users.items():

        size = len(arr)
        if n > size:
            continue

        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)

        for i in range(n, size, k):
            if i + k > size:
                break
            input = udata[arr[i: i + k]]
            input = reliable_bits(input, index)
            intra += [distance(input, entry)]

        for iv, brr in users.items():

            size = len(brr)
            if ix == iv:
                continue

            for i in range(0, size, k):
                if i + k > size:
                    break
                input = udata[brr[i: i + k]]
                input = reliable_bits(input, index)
                inter += [distance(input, entry)]

    return intra, inter


def mean_error_rate_full():
    start = 0
    end = 511

    users = enumerate_users()

    intra = []
    inter = []

    for ix, arr in users.items():

        size = len(arr)
        if n > size:
            continue

        entry = udata[arr[:n]]
        entry = binarization(entry, start, end)

        for i in range(n, size, k):
            if i + k > size:
                break
            input = udata[arr[i: i + k]]
            input = binarization(input, start, end)
            intra += [distance(input, entry)]

        for iv, brr in users.items():

            size = len(brr)
            if ix == iv:
                continue

            for i in range(0, size, k):
                if i + k > size:
                    break
                input = udata[brr[i: i + k]]
                input = binarization(input, start, end)
                inter += [distance(input, entry)]

    return intra, inter


def mean_false_rate(usr_id: int, ip: int):

    users = enumerate_users()

    intra = inter = 0

    for rate in [0.20, 0.25, 0.30]:

        extractor = SampleLock(rate, 256)

        print(f'extractor with error {rate}:')

        for ix, arr in users.items():

            if ix != usr_id:
                continue
            if n > len(arr):
                continue

            entry = udata[arr[:n]]
            index = reliable_index(entry)
            entry = reliable_bits(entry, index)
            entry = extractor.generate(entry)

            for i in range(n, len(arr), k):
                if i + k > len(arr):
                    break
                input = udata[arr[i: i + k]]
                input = reliable_bits(input, index)
                input = extractor.reproduce(input)
                intra += (entry != input)

            print(f'check user {ix} intra error: {intra}')

            sign = False
            for iv, brr in users.items():
                if iv == ip:
                    sign = True
                if not sign:
                    continue
                if ix == iv:
                    continue
                input = udata[random.sample(brr, k)]
                input = reliable_bits(input, index)
                input = extractor.reproduce(input)
                inter += (entry == input)

                print(f'inter error with user {iv}: {inter}')

    return intra, inter


def plot_reliable():

    jdata = '../json/error_' + plot_name + '_reliable.json'
    ifile = '../plot/plot_' + plot_name + '_reliable.png'

    intra, inter = mean_error_rate()

    save_error(intra, inter, jdata)
    visualize_The(jdata, ifile, 1.0, 0.01, 1.0, 0.15)


def plot_full():

    jdata = '../json/error_' + plot_name + '_full.json'
    ifile = '../plot/plot_' + plot_name + '_full.png'

    intra, inter = mean_error_rate_full()

    save_error(intra, inter, jdata)
    visualize_The(jdata, ifile, 1.0, 0.01, 1.0, 0.15)


def mean_error_rate_random():

    users = enumerate_users()

    intra = []
    inter = []

    for ix, arr in users.items():

        size = len(arr)
        if n > size:
            continue

        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)

        input = udata[np.random.choice(arr[n:size], k)]
        input = reliable_bits(input, index)
        intra += [distance(input, entry)]

        for iv, brr in users.items():

            size = len(brr)
            if ix == iv:
                continue
            if k > size:
                continue

            input = udata[np.random.choice(brr, k)]
            input = reliable_bits(input, index)
            inter += [distance(input, entry)]

    return intra, inter


def cal_error_full():
    intra, inter = mean_error_rate_full()

    cnt_intra = 0
    for val in intra:
        if (val > 0.2):
            cnt_intra += 1
    print("Full:")
    print(cnt_intra)
    print(len(intra))

    cnt_inter = 0
    for val in inter:
        if (val < 0.2):
            cnt_inter += 1
            print(val)
    print(cnt_inter)
    print(len(inter))


def cal_error_reliable():
    print("Reliable:")

    total_inter = 0
    total_intra = 0

    for _ in range(l):
        intra, inter = mean_error_rate_random()

        for val in intra:
            if (val > 0.2):
                total_intra += 1

        for val in inter:
            if (val < 0.2):
                total_inter += 1

    total_intra /= l
    total_inter /= l

    print(total_intra)
    print(total_inter)


cal_error_reliable()
