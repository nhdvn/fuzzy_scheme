
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

    user = enumerate_users()
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
