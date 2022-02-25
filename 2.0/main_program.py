
import time
from help_function import *
from fuzzy_scheme import *


extractor = SampleLock(0.2, 512)


def generate_key(idx_template: list):

    entry = udata[idx_template[:5]]
    index = reliable_index(entry)
    entry = reliable_bits(entry, index)
    value = extractor.generate(entry)
    return value, index 


def reproduce_key(idx_template: list, index: list):

    entry = udata[idx_template[5:8]]
    entry = reliable_bits(entry, index)
    return extractor.reproduce(entry)


def main():

    user = enumerate_users()
    user_31 = user[31]
    user_34 = user[34]

    start = time.time()
    key, index = generate_key(user_31)
    finis = time.time()

    print(finis - start)
    print(key)

    start = time.time()    
    key = reproduce_key(user_31, index)
    finis = time.time()
    
    print(finis - start)
    print(key)


main()