
import hashlib, secrets


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
