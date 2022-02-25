
import json, os, random
from digital_locker import DigitalLocker


class SampleLock:

    index = list(range(512))
    locker = DigitalLocker(224, 128, 144, 80)
    ksize = 16
    wbits = 80
    bound = None


    def __init__(self, _bound) -> None:
        self.bound = _bound


    def generate(self, bio: str):
        
        key = os.urandom(self.ksize)
        pub = open('01.helper', 'w')

        for _ in range(self.bound):

            idx = random.sample(self.index, self.wbits)
            sub = ''.join([bio[i] for i in idx])
            
            pair = self.locker.lock(sub, key)
            iv = (pair, idx)

            pub.write(json.dumps(iv) + '\n')

        pub.close()

        return key


    def reproduce(self, bio: str):

        pub = open('01.helper', 'r')

        for _ in range(self.bound):

            line = pub.readline()
            pair, idx = json.loads(line)

            sub = ''.join([bio[i] for i in idx])
            key = self.locker.unlock(sub, pair)

            if key != b'Error': break

        pub.close()

        return key
