
import numpy
import FuzzyScheme


class VoiceCryptoSystem:

    def __init__(self):
        
        self.template_size = 512
        self.reliable_size = 256
        self.extractor = FuzzyScheme.SampleLock(2, 0.2, 256)
        self.ivstorage = {}


    def enroll_user(self, user: int, vdata: numpy.ndarray):

        index = self.select_reliable_index(vdata)
        self.ivstorage[user] = index
        input = self.extract_reliable_bits(vdata, index)
        return self.extractor.key_generate(user, input)


    def verify_user(self, user: int, vdata: numpy.ndarray):

        index = self.ivstorage[user]
        input = self.extract_reliable_bits(vdata, index)
        return self.extractor.key_reproduce(user, input)


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