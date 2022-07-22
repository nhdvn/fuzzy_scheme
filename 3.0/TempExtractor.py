
import os
import numpy
import random
import matplotlib.pyplot as matplot
import seaborn


dataset = {

    "vkyc_nht": {
        "d_path": os.path.join("..", "data", "Nhut"),
        "n_size": 256,
        "r_size": 256,
        "id_pos": 0,
    },

    "vkyc_the": {
        "d_path": os.path.join("..", "data", "The"),
        "n_size": 512,
        "r_size": 256,
        "id_pos": -1
    },

    "timit_39_300": {
        "d_path": os.path.join("..", "data", "Timit_39_300"),
        "n_size": 512,
        "r_size": 256,
        "id_pos": -1
    },

    "timit_39_400": {
        "d_path": os.path.join("..", "data", "Timit_39_400"),
        "n_size": 512,
        "r_size": 256,
        "id_pos": -1
    },

    "timit_47_400": {
        "d_path": os.path.join("..", "data", "Timit_47_400"),
        "n_size": 512,
        "r_size": 256,
        "id_pos": -1
    },
}


class VoiceTemplateLoader:

    def __init__(self, dataset: dict):

        self.n_data = numpy.genfromtxt(dataset['d_path'], delimiter=',')

        self.id_pos = dataset['id_pos']
        self.n_size = dataset['n_size']
        self.r_size = dataset['r_size']

        self.d_list = self.enumerate_data()
        self.u_list = list(self.d_list.keys())

    def enumerate_data(self) -> dict:

        res = {}

        for i, row in enumerate(self.n_data):

            u = int(row[self.id_pos])  # index of uid in the vector

            if u not in res:
                res[u] = []

            res[u] += [i]  # store index of vector for reuse

        return res

    def load_user_data(self, uid: int, n: int) -> list:

        row = self.d_list[uid]

        return self.n_data[random.sample(row, n)]

    def binary_distance(self, x: list, y: list) -> float:

        count = 0

        for a, b in zip(x, y):
            if a != b:
                count += 1

        return count / len(x)

    def reliable_index(self, data: numpy.ndarray):

        result = []

        for i in range(self.n_size):
            mean = data[:, i].mean()
            dist = data[:, i] - mean
            vari = (dist ** 2).sum()
            result.append(vari)

        return numpy.argsort(result)[:self.r_size]

    def reliable_bits(self, data: numpy.ndarray, index: list):

        res = ''
        mean = numpy.mean(data, axis=0)

        for val in mean[index]:
            res += '0' if val <= 0 else '1'

        return res

    def mean_distance(self, n: int, k: int):

        intra = []
        inter = []

        for ix, arr in self.d_list.items():

            size = len(arr)
            if n > size:
                continue

            entry = self.n_data[arr[:n]]
            index = self.reliable_index(entry)
            entry = self.reliable_bits(entry, index)

            for i in range(n, size, k):
                if i + k > size:
                    break

                input = self.n_data[arr[i: i + k]]
                input = self.reliable_bits(input, index)
                error = self.binary_distance(input, entry)
                intra += [error]

            for iv, brr in self.d_list.items():

                size = len(brr)
                if ix == iv:
                    continue

                for i in range(0, size, k):
                    if i + k > size:
                        break

                    input = self.n_data[brr[i: i + k]]
                    input = self.reliable_bits(input, index)
                    error = self.binary_distance(input, entry)
                    inter += [error]

        return intra, inter

    def visualize(ifile: str, intra, inter, xmax: float, ymax: float):

        matplot.rcParams["figure.figsize"] = [7.00, 3.50]
        matplot.rcParams["figure.autolayout"] = True

        fig, x_axis = matplot.subplots()

        seaborn.set(style="darkgrid", rc={
            'axes.edgecolor': 'black', 'axes.linewidth': 0.25})
        seaborn.histplot(intra, binrange=(0, 1), binwidth=0.01,
                         ax=x_axis, kde=False, stat='probability', label='Intra-class', color='blue')
        seaborn.histplot(inter, binrange=(0, 1), binwidth=0.01,
                         ax=x_axis, kde=False, stat='probability', label='Inter-class', color='crimson')

        matplot.legend()
        matplot.xlabel("Hamming Distance Threshold")
        matplot.grid(True)

        x_axis.set_xlim([0, xmax])
        x_axis.set_ylim([0, ymax])

        matplot.savefig(ifile)
