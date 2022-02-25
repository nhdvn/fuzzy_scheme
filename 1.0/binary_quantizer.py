
import numpy as np

class Quantizer:

    def __init__(self) -> None:
        pass
        

    def sign(self, features: list) -> str:
        
        res = ''

        for each in features:
            if each > 0: res += '1'
            if each < 0: res += '0'

        return res

    
    def bytes(self, features: np.ndarray) -> bytes:

        bits = self.sign(features)

        size = (len(bits) + 7) // 8

        return int(bits, 2).to_bytes(size, byteorder = 'big')