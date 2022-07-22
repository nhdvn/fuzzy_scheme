
import time
from help_function import *
from fuzzy_scheme import *


extractor = SampleLock(0.2, 512)


def generate_key(row: list):

    entry = udata[row[:5]]
    index = reliable_index(entry)
    entry = reliable_bits(entry, index)
    value = extractor.generate(entry)
    return value, index


def reproduce_key(row: list, index: list):

    entry = udata[row[0:3]]
    entry = reliable_bits(entry, index)
    return extractor.reproduce(entry)


def main():

    users = enumerate_users()
    res = [0] * 7
    limit = [10, 20, 40, 70, 100, 150, 10000]
    a = []
    for user, ids in users.items():
        for i in range(7):
            if (len(ids) < limit[i]):
                res[i] += 1
                break
        print(str(user) + ': ' + str(len(ids)))
        a.append(len(ids))
    print(a)
    a.sort()
    print(a)
    print(res)

    return()
    user_x = user[46]
    user_v = user[100]

    start = time.time()
    key, index = generate_key(user_x)
    finis = time.time()

    print(finis - start)
    print(key)

    start = time.time()
    key = reproduce_key(user_v, index)
    finis = time.time()

    print(finis - start)
    print(key)


main()
