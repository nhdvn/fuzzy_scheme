
import hashlib
import math
import multiprocessing
import os
import random


class DigitalLocker:

    def __init__(self, _N, _K, _R):

        self.N = _N  # 28 bytes - 224 bits hash
        self.K = _K  # 16 bytes - 128 bits secret
        self.R = _R  # 18 bytes - 144 bits nonce
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

        if vlock[self.K:] == self.P:
            return vlock[:self.K]


class SampleLock:

    def __init__(self, div: int, rate: float, size: int):

        self.locker = DigitalLocker(28, 16, 18)
        self.div_size = div
        self.key_size = 16
        self.sub_size = 80
        self.pub_size = 126  # = 80 + 46

        self.bound = math.floor(math.exp(rate * self.sub_size)) // div
        self.range = range(size)

    def bits_to_bytes(self, bio: str, idx: list):

        subset = "".join([bio[i] for i in idx])

        return int(subset, 2).to_bytes(10, "big")

    def array_to_bytes(self, idx: list, bio: str):

        return bytes(idx), self.bits_to_bytes(bio, idx)

    def public_to_bytes(self, arr: bytes, bio: str):

        return self.bits_to_bytes(bio, [i for i in arr])

    def key_generate(self, user: int, bio: str):

        secret = os.urandom(self.key_size)
        handler = multiprocessing.Pool(self.div_size)

        for i in range(self.div_size):
            params = (user, bio, i, secret)
            handler.apply_async(self.worker_gen, params)

        handler.close()
        handler.join()
        return secret

    def key_reproduce(self, user: int, bio: str):

        manager = multiprocessing.Manager()
        handler = multiprocessing.Pool(self.div_size)
        result = manager.dict()

        def terminate(result):
            if result:
                handler.terminate()

        for i in range(self.div_size):
            params = (user, bio, i, result)
            handler.apply_async(
                self.worker_rep, args=params, callback=terminate)

        handler.close()
        handler.join()

        for secret in result.values():
            if secret != None:
                return secret
        return None

    def worker_gen(self, user: int, input: str, nth: int, secret: bytes):

        helper = open(os.path.join("..", "public", f"_{nth}"), "wb")

        for _ in range(self.bound):

            index = random.sample(self.range, self.sub_size)
            index, subset = self.array_to_bytes(index, input)
            vlock = self.locker.lock(subset, secret)
            helper.write(index + vlock)

        helper.close()

    def worker_rep(self, user: int, input: str, nth: int, result: dict):

        helper = open(os.path.join("..", "public", f"_{nth}"), "rb")

        for _ in range(self.bound):

            block = helper.read(self.pub_size)
            index = block[:self.sub_size]
            vlock = block[self.sub_size:]

            subset = self.public_to_bytes(index, input)
            secret = self.locker.unlock(subset, vlock)
            if secret:
                break

        helper.close()
        result[nth] = secret
        return secret
