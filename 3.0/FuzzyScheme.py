
import math
import random
import hashlib
import secrets


class DigitalLocker:

    N = None # 28 bytes - 224 bits hash
    K = None # 16 bytes - 128 bits secret
    R = None # 18 bytes - 144 bits nonce


    def __init__(self, _N, _K, _R):
        self.N = _N
        self.K = _K
        self.R = _R
        self.P = bytes(self.N - self.K)


    def xor(self, b1: bytes, b2: bytes) -> bytes:

        val = int.from_bytes(b1, 'big') ^ int.from_bytes(b2, 'big')

        return val.to_bytes(self.N, 'big')


    def lock(self, key: bytes, value: bytes) -> bytes:

        nonce = secrets.token_bytes(self.R)

        vhash = hashlib.new('SHA224', nonce + key).digest()

        return nonce + self.xor(vhash, value + self.P)


    def unlock(self, key: bytes, data: bytes) -> bytes:

        nonce, vlock = data[:self.R], data[self.R:]

        vhash = hashlib.new('SHA224', nonce + key).digest()

        vlock = self.xor(vhash, vlock)

        if vlock[self.K:] == self.P: return vlock[:self.K]



class SampleLock:

    locker = DigitalLocker(28, 16, 18)
    nbytes = 16
    strlen = 80


    def __init__(self, rate, size) -> None:
        self.bound = math.floor(math.exp(rate * self.strlen))
        self.range = range(size)


    def bit_to_bytes(self, bio: str, idx: list):

        return int(str.join('', [bio[i] for i in idx]), 2).to_bytes(10, 'big')


    def arr_to_bytes(self, bio: str, idx: list):

        idx_bytes = bytes.join(b'', [i.to_bytes(2, 'big') for i in idx])

        return idx_bytes, self.bit_to_bytes(bio, idx)


    def arr_from_bytes(self, bio: str, arr: bytes):

        idx = [int.from_bytes(arr[i: i + 2], 'big') for i in range(0, 160, 2)]

        return self.bit_to_bytes(bio, idx)


    def key_generate(self, uid: int, bio: str):

        secret = secrets.token_bytes(self.nbytes)
        helper = open(f'./Helper_{uid}', 'wb')

        for _ in range(self.bound):

            idx = random.sample(self.range, self.strlen)
            idx, sub = self.arr_to_bytes(bio, idx)
            buffer = idx + self.locker.lock(sub, secret)
            helper.write(buffer)

        helper.close()
        return secret


    def key_reproduce(self, uid: int, bio: str):

        helper = open(f'./Helper_{uid}', 'rb')

        for _ in range(self.bound):

            block = helper.read(206)
            idx, val = block[:160], block[160:]
            sub = self.arr_from_bytes(bio, idx)
            secret = self.locker.unlock(sub, val)

            if secret != None: break

        helper.close()
        return secret
