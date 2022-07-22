
import numpy
import FuzzyScheme as FuzzyScheme


class VoiceCryptoSystem:

    def __init__(self, dataset: dict):

        self.id_pos = dataset['id_pos']
        self.n_size = dataset['n_size']
        self.r_size = dataset['r_size']
        self.extractor = FuzzyScheme.SampleLock(4, 0.2, self.r_size)
        self.reliables = {}

    def enroll_user(self, user: int, data: numpy.ndarray):

        index = self.select_reliable_index(data)
        self.reliables[user] = index
        input = self.extract_reliable_bits(data, index)
        return self.extractor.key_generate(user, input)

    def verify_user(self, user: int, data: numpy.ndarray):

        index = self.reliables[user]
        input = self.extract_reliable_bits(data, index)
        return self.extractor.key_reproduce(user, input)

    def select_reliable_index(self, data: numpy.ndarray):

        result = []

        for i in range(self.n_size):
            mean = data[:, i].mean()
            dist = data[:, i] - mean
            vari = (dist ** 2).sum()
            result.append(vari)

        return numpy.argsort(result)[:self.r_size]

    def extract_reliable_bits(self, data: numpy.ndarray, index: list):

        res = ''
        mean = numpy.mean(data, axis=0)

        for val in mean[index]:
            res += '0' if val <= 0 else '1'

        return res
