
import numpy
import FuzzyScheme


class VoiceCryptoSystem:

    def __init__(self, size):
        
        self.template_size = size
        self.reliable_size = size >> 1
        self.extractor = FuzzyScheme.SampleLock(0.2, size >> 1)
        self.storage = {}


    def enroll_user(self, uid: int, vdata: list):

        index = self.select_reliable_index(vdata)
        self.storage[uid] = index
        input = self.extract_reliable_bits(vdata, index)
        return self.extractor.key_generate(uid, input)


    def verify_user(self, uid: int, vdata: list):

        index = self.storage[uid]
        input = self.extract_reliable_bits(vdata, index)
        return self.extractor.key_reproduce(uid, input)


    def select_reliable_index(self, vdata: numpy.ndarray):

        result = []

        for i in range(self.template_size):
            mean = vdata[:, i].mean()
            dist = vdata[:, i] - mean
            vari = (dist ** 2).sum()
            result.append(vari)

        return numpy.argsort(result)[:self.reliable_size]


    def extract_reliable_bits(self, vdata: numpy.ndarray, index: list):

        res = ''
        mean = vdata.mean(axis = 0)

        for val in mean[index]:
            res += '0' if val <= 0 else '1'

        return res