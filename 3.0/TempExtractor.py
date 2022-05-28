
import numpy
import random


class VoiceTemplate:

    def __init__(self):

        self.udata = numpy.genfromtxt("../data/The", delimiter = ',')
        
        self.ulist = self.enumerate_users()


    def enumerate_users(self) -> dict:

        res = {}
        
        for i, row in enumerate(self.udata):

            u = int(row[-1])

            if u not in res: res[u] = []

            res[u] += [i]

        return res


    def load_user_template(self, uid: int, k: int) -> list:

        index = self.ulist[uid]
        
        return self.udata[random.sample(index, k)]
