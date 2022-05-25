import os
import sys
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 5  # number of entry
k = 3  # number of valid

users = enumerate_users()
ulist = list(users.keys())

ifile = "/content/drive/MyDrive/Index"
inter = "/content/drive/MyDrive/Inter"
ufile = None


def iter_position(id: int):

    dir = f"{inter}/{id}"

    global ufile

    if os.path.isfile(dir):
        ufile = open(dir, 'a')
        return len(open(dir, 'r').readlines())

    ufile = open(dir, 'w')
    return 0


def update_file(usr, val=None):

    ufile.write(f'{usr}: {val}\n')


def save_drive(arr):

    os.system(
        'cp /content/fuzzy_scheme/data/helper_data /content/drive/MyDrive/Helper')

    open(ifile, 'w').write(str(list(arr)))


def load_drive():

    os.system(
        'cp /content/drive/MyDrive/Helper /content/fuzzy_scheme/data/helper_data')

    return json.loads(open(ifile, 'r').read())


def mean_false_rate(ix: int):

    extractor = SampleLock(0.2, 256)

    arr = users[ix]
    if n > len(arr):
        return print('no need')

    itr = iter_position(ix)
    if itr == len(ulist):
        return print('finish')

    if os.path.isfile(ifile):
        index = load_drive()
    else:
        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)
        entry = extractor.generate(entry)
        save_drive(index)

    for iv in ulist[itr:]:
        print(iv)
        if ix == iv:
            update_file(iv)
        else:
            input = udata[random.sample(users[iv], k)]
            input = reliable_bits(input, index)
            input = extractor.reproduce(input)
            update_file(iv, entry == input)


mean_false_rate(int(sys.argv[1]))
