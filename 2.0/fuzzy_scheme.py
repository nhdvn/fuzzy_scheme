
import math, random, secrets
from digital_locker import *


class SampleLock:

    locker = DigitalLocker(28, 16, 18)
    nbytes = 16
    strlen = 80


    def __init__(self, rate, size) -> None:
        self.bound = math.floor(math.exp(rate * self.strlen))
        self.range = range(size)


    def bit_to_bytes(self, bio: str, idx: list):

        return int(str.join('', [bio[i] for i in idx]), 2).to_bytes(10, 'big')


    def arr_to_bytes(self, bio: str, idx: list[int]):

        arr = bytes.join(b'', [i.to_bytes(2, 'big') for i in idx])

        return arr, self.bit_to_bytes(bio, idx)


    def arr_from_bytes(self, bio: str, arr: bytes):

        idx = [int.from_bytes(arr[i: i + 2], 'big') for i in range(0, 160, 2)]

        return self.bit_to_bytes(bio, idx)


    def generate(self, bio: str):

        secret = secrets.token_bytes(self.nbytes)
        helper = open('../data/helper_data', 'wb')

        for _ in range(self.bound):

            idx = random.sample(self.range, self.strlen)
            idx, sub = self.arr_to_bytes(bio, idx)
            buffer = idx + self.locker.lock(sub, secret)
            helper.write(buffer)

        helper.close()
        return secret


    def reproduce(self, bio: str):

        helper = open('../data/helper_data', 'rb')

        for _ in range(self.bound):

            block = helper.read(206)
            idx, val = block[:160], block[160:]
            sub = self.arr_from_bytes(bio, idx)
            secret = self.locker.unlock(sub, val)

            if secret != None: break

        helper.close()
        return secret
