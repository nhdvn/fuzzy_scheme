
import hashlib, secrets


class DigitalLocker:

    N = None # 28 bytes - 224 bits hash
    K = None # 16 bytes - 128 bits secret
    R = None # 18 bytes - 144 bits nonce


    def __init__(self, _N, _K, _R):
        self.N = _N
        self.K = _K
        self.R = _R


    def xor(self, b1: bytes, b2: bytes) -> bytes:

        return bytes( [x1 ^ x2 for x1, x2 in zip(b1, b2)] )


    def lock(self, key: bytes, value: bytes) -> bytes:

        nonce, vhash = self.hash(key)

        value = value.ljust(self.N, b'\x00')

        vlock = self.xor(vhash, value)

        return nonce + vlock


    def unlock(self, key: bytes, data: bytes) -> bytes:

        nonce = data[:self.R]
        vlock = data[self.R:]

        nonce, vhash = self.hash(key, nonce)
        value = self.xor(vhash, vlock)

        if value[self.K:].rstrip(b'\x00'): return None
        
        return value[:self.K]


    def hash(self, value: bytes, nonce: bytes = b'') -> tuple:
        
        if not nonce: 
            nonce = secrets.token_bytes(self.R)

        hash = hashlib.new('SHA224', nonce + value)

        return nonce, hash.digest()
