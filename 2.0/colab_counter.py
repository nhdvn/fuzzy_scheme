
from os.path import isfile
from random import sample
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 5 # number of entry
k = 3 # number of valid

users = enumerate_users()
ulist = users.keys()
ksize = 225
ufile = None


def iter_position(id: int):
    
    dir = f'/content/drive/MyDrive/Inter/{id}'

    global ufile

    if isfile(dir):
        ufile = open(dir, 'a')
        return len(open(dir, 'r').readlines())

    ufile = open(dir, 'w')
    return 0


def update_file(usr, val = None):

    ufile.write(f'{usr}: {val}\n')


def mean_false_rate():

    extractor = SampleLock(0.2, 512)

    for ix, arr in users.items():

        itr = iter_position(ix)
        if itr == ksize: continue
        if n > len(arr): continue

        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)
        entry = extractor.generate(entry)

        for iv in ulist[itr:]:
            if ix == iv: 
                update_file(iv)
            else:
                input = udata[sample(users[iv], k)]
                input = reliable_bits(input, index)
                input = extractor.reproduce(input)
                update_file(iv, entry == input)