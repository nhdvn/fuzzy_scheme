
import numpy, random


class VoiceTemplate:


    def __init__(self) -> None:

        self.udata = numpy.genfromtxt('../data/The', delimiter = ',')
        self.ulist = self.enumerate_users()


    def enumerate_users(self) -> dict:

        result = {}
        
        for row, data in enumerate(self.udata):

            user = int(data[-1])

            if user not in result:
                result[user] = []

            result[user] += [row]

        return result


    def load_user_template(self, uid: int, nT: int):

        user = self.ulist[uid]
        
        return random.sample(user, nT)
