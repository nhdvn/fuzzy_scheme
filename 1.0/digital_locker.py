from Crypto.Hash import SHA224
from Crypto.Random import urandom


class DigitalLocker:

    H = SHA224
    N = None # n bits of hash (default = 224)
    K = None # k bits of secret key
    R = None # r bits of nonce
    W = None # w bits of bio subset
    P = None # padding sequence (224 - 128 = 96)


    def __init__(self, n, k, r, w) -> None:
        self.N = n // 8
        self.K = k // 8
        self.W = w // 8
        self.R = r // 8
        self.P = b'\x00' * (self.N - self.K)


    def bits_to_bytes(self, bits: str) -> bytes:

        return int(bits, 2).to_bytes(self.W, byteorder = 'big')


    def pad(self, arr_bytes: bytes) -> bytes:

        return arr_bytes + self.P


    def unpad(self, arr_bytes: bytes) -> bytes:

        val = arr_bytes[:self.K]
        pad = arr_bytes[self.K:]

        if int.from_bytes(pad, 'big') == 0:
            return val
        else:
            return b'Error'


    def xor(self, b1: bytes, b2: bytes) -> bytes:

        return bytes( [x1 ^ x2 for x1, x2 in zip(b1, b2)] )


    def lock(self, key: str, value: bytes) -> tuple:

        key = self.bits_to_bytes(key)
        nonce, vhash = self.hash(key)
        value = value + self.P
        vlock = self.xor(vhash, value)

        return nonce.hex(), vlock.hex()


    def unlock(self, key: str, lock_pair) -> bytes:

        nonce, vlock = lock_pair
        nonce = bytes.fromhex(nonce)
        vlock = bytes.fromhex(vlock)

        key = self.bits_to_bytes(key)
        nonce, vhash = self.hash(key, nonce)
        value = self.xor(vhash, vlock)

        return self.unpad(value)


    def hash(self, key: bytes, nonce: bytes = b'') -> tuple:
        
        if not nonce: 
            nonce = urandom(self.R)

        hash = self.H.new(nonce)
        hash.update(key)
        vhash = hash.digest()

        return (nonce, vhash)
