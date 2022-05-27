
import math
import hashlib
import os
import random


class DigitalLocker:

    def __init__(self, _N, _K, _R):
        
        self.N = _N # 28 bytes - 224 bits hash
        self.K = _K # 16 bytes - 128 bits secret
        self.R = _R # 18 bytes - 144 bits nonce
        
        self.P = bytes(self.N - self.K)


    def xor(self, b1: bytes, b2: bytes) -> bytes:

        val = int.from_bytes(b1, "big") ^ int.from_bytes(b2, "big")

        return val.to_bytes(self.N, "big")


    def lock(self, key: bytes, value: bytes) -> bytes:

        nonce = os.urandom(self.R)

        vhash = hashlib.sha224(nonce + key).digest()

        return nonce + self.xor(vhash, value + self.P)


    def unlock(self, key: bytes, data: bytes) -> bytes:

        nonce, vlock = data[:self.R], data[self.R:]

        vhash = hashlib.sha224(nonce + key).digest()

        vlock = self.xor(vhash, vlock)

        if vlock[self.K:] == self.P: return vlock[:self.K]



class SampleLock:

    def __init__(self, rate, size):

        self.locker = DigitalLocker(28, 16, 18)
        self.key_size = 16
        self.sub_size = 80
        self.pub_size = 126 # = 80 + 46
        
        self.bound = math.floor(math.exp(rate * self.sub_size))
        self.range = range(size)


    def bits_to_bytes(self, bio: str, idx: list):

        subset = "".join([bio[i] for i in idx])

        return int(subset, 2).to_bytes(10, "big")


    def array_to_bytes(self, idx: list, bio: str):

        return bytes(idx), self.bits_to_bytes(bio, idx)


    def public_to_bytes(self, arr: bytes, bio: str):

        return self.bits_to_bytes(bio, [i for i in arr])


    def random_subset(self):

        return random.sample(self.range, self.sub_size)


    def key_generate(self, ID: int, bio: str):

        secret = os.urandom(self.key_size)
        helper = open(f"./Helper_{ID}", "wb")

        for _ in range(self.bound):

            idx = self.random_subset()
            idx, sub = self.array_to_bytes(idx, bio)
            vlocked = self.locker.lock(sub, secret)
            helper.write(idx + vlocked)

        helper.close()
        return secret


    def key_reproduce(self, ID: int, bio: str):

        helper = open(f"./Helper_{ID}", "rb")

        while block := helper.read(self.pub_size):
            
            idx = block[:self.sub_size]
            val = block[self.sub_size:]
            sub = self.public_to_bytes(idx, bio)
            secret = self.locker.unlock(sub, val)
            if secret != None: break

        helper.close()
        return secret
