
import numpy
import FuzzyScheme


class VoiceCryptoSystem:

    extractor = FuzzyScheme.SampleLock(0.2, 256)
    ivstorage = {}


    def __init__(self) -> None:
        pass


    def enroll_user(self, uid: int, sample: list):

        index = self.select_reliable_index(sample)
        self.ivstorage[uid] = index
        input = self.extract_reliable_bits(sample, index)
        return self.extractor.key_generate(uid, input)


    def verify_user(self, uid: int, sample: list):

        index = self.ivstorage[uid]
        input = self.extract_reliable_bits(sample, index)
        return self.extractor.key_reproduce(uid, input)


    def select_reliable_index(self, data: numpy.ndarray):

        result = []

        for i in range(512):
            mean = data[:, i].mean()
            diff = data[:, i] - mean
            sqrs = (diff ** 2).sum()
            result.append(sqrs)

        return numpy.argsort(result)[:256]


    def extract_reliable_bits(data: numpy.ndarray, index: list):

        res = ''
        mean = data.mean(axis = 0)

        for val in mean[index]:
            res += '0' if val <= 0 else '1'

        return res