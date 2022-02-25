
from help_function import *

qdata = []
nbits = 512
fname = format(nbits, '04d')


def binarize_udata():

    global qdata

    for row in udata:
        res = reliable_bits(row[:-1])
        qdata += [res]


def distance(x, y): # hamming distance
    
    count = 0
    
    for xbit, ybit in zip(x, y):
        if xbit != ybit: count = count + 1
    
    return count / nbits


def intra_error(arr):

    ans = []
    size = len(arr)

    for u in range(0, size):
        for v in range(u + 1, size):
            ans += [distance(qdata[arr[u]], qdata[arr[v]])]

    return ans


def inter_error(arr, brr):

    ans = []

    for u in arr:
        for v in brr:
            ans += [distance(qdata[u] , qdata[v])]

    return ans


def pairwise_error():

    binarize_udata()

    users = enumerate_users()
    intra = inter = finis = []

    for i in users:
        intra += intra_error(users[i])
        finis += [i]
        for j in users:
            if j in finis: continue
            inter += inter_error(users[i], users[j])

    save_error(intra, inter)