
import numpy
import random


class VoiceTemplateLoader:

    def __init__(self):

        self.ndata = numpy.genfromtxt("../data/Nhut", delimiter=',')

        self.dlist = self.enumerate_data()

        self.ulist = list(self.dlist.keys())

    def enumerate_data(self) -> dict:

        res = {}

        for i, row in enumerate(self.ndata):

            u = int(row[0])

            if u not in res:
                res[u] = []

            res[u] += [i]

        return res

    def load_user_data(self, uid: int, n: int) -> list:

        rlist = self.dlist[uid]

        return self.ndata[random.sample(rlist, n)]
