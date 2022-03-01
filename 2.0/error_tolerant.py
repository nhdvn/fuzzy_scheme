
from sys import argv
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 5 # number of entry
k = 3 # number of valid


def mean_error_rate():

    users = enumerate_users()

    intra = []
    inter = []

    for ix, arr in users.items():
        
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

        for iv, brr in users.items():

            size = len(brr)
            if ix == iv: continue

            for i in range(0, size, k):
                if i + k > size: break
                input = udata[brr[i: i + k]]
                input = reliable_bits(input, index)
                inter += [distance(input, entry)]

    return intra, inter


def mean_false_rate(usr_id: int, ip: int):

    users = enumerate_users()

    intra = inter = 0

    for rate in [0.20, 0.25, 0.30]:

        extractor = SampleLock(rate, 512)

        print(f'extractor with error {rate}:')

        for ix, arr in users.items():

            if ix != usr_id: continue
            if n > len(arr): continue

            entry = udata[arr[:n]]
            index = reliable_index(entry)
            entry = reliable_bits(entry, index)
            entry = extractor.generate(entry)

            for i in range(n, len(arr), k):
                if i + k > len(arr): break
                input = udata[arr[i: i + k]]
                input = reliable_bits(input, index)
                input = extractor.reproduce(input)
                intra += (entry != input)

            print(f'check user {ix} intra error: {intra}')

            sign = False
            for iv, brr in users.items():
                if iv == ip: sign = True
                if not sign: continue
                if ix == iv: continue
                input = udata[random.sample(brr, k)]
                input = reliable_bits(input, index)
                input = extractor.reproduce(input)
                inter += (entry == input)

                print(f'inter error with user {iv}: {inter}')
    
    return intra, inter


def main():

    jdata = '../json/error_0512.json'
    ifile = '../plot/plot_0512.png'

    intra, inter = mean_error_rate()
    
    save_error(intra, inter, jdata)
    visualize(jdata, ifile)


mean_false_rate(int(argv[1]), int(argv[2]))