import os
import sys
from help_function import *
from fuzzy_scheme import *
from error_visualize import *

n = 5  # number of entry
k = 3  # number of valid

users = enumerate_users()
ulist = list(users.keys())

inter = "/content/drive/MyDrive/Inter"
ibyte = "/content/drive/MyDrive/Entry"
ifile = "/content/drive/MyDrive/Index"
ihelp = "/content/drive/MyDrive/Helper"
hdata = "/content/fuzzy_scheme/data/helper_data"
ufile = None

save_helper = f"cp {hdata} {ihelp}"
load_helper = f"cp {ihelp} {hdata}"


def iter_position(id: int):

    dir = f"{inter}/{id}"

    global ufile

    if os.path.isfile(dir):
        ufile = open(dir, 'a')
        return len(open(dir, 'r').readlines())

    ufile = open(dir, 'w')
    return 0


def update_file(usr, val=None):

    print(val)

    ufile.write(f'{usr}: {val}\n')


def save_drive(arr, entry: bytes):

    os.system(save_helper)

    open(ibyte, 'wb').write(entry)

    open(ifile, 'w').write(str(list(arr)))


def load_drive():

    os.system(load_helper)

    entry = open(ibyte, 'rb').read()

    arr = json.loads(open(ifile, 'r').read())

    return arr, entry


def mean_false_rate(ix: int):

    extractor = SampleLock(0.2, 256)

    arr = users[ix]

    if n > len(arr):
        return print('no need')

    itr = iter_position(ix)

    if itr == len(ulist):
        return print('finish')

    if itr == 0:
        if os.path.exists(ifile):
            os.remove(ifile)
        if os.path.exists(ibyte):
            os.remove(ibyte)
        if os.path.exists(ihelp):
            os.remove(ihelp)

    if os.path.isfile(ifile):
        index, entry = load_drive()
    else:
        entry = udata[arr[:n]]
        index = reliable_index(entry)
        entry = reliable_bits(entry, index)
        entry = extractor.generate(entry)
        save_drive(index, entry)

    for iv in ulist[itr:]:
        print(iv, end=' ')
        if ix == iv:
            update_file(iv)
        else:
            input = udata[random.sample(users[iv], k)]
            input = reliable_bits(input, index)
            input = extractor.reproduce(input)
            update_file(iv, entry == input)


mean_false_rate(int(sys.argv[1]))
