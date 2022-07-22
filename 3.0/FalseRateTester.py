
import os
import json
from TempExtractor import VoiceTemplateLoader
from CryptoSystem import VoiceCryptoSystem


inter = "/content/drive/MyDrive/Inter"
ibyte = "/content/drive/MyDrive/Entry"
ifile = "/content/drive/MyDrive/Index"
ihelp = "/content/drive/MyDrive/Helper"
hdata = "/content/fuzzy_scheme/data/helper_data"

save_helper = f"cp {hdata} {ihelp}"
load_helper = f"cp {ihelp} {hdata}"


class FalseRateTester:

    def __init__(self, dataset: dict):
        self.N = 5
        self.K = 3
        self.system = VoiceCryptoSystem(dataset['n_size'], dataset['r_size'])
        self.module = VoiceTemplateLoader(dataset)
        self.output = None

    def update_output(self, usr, val):

        self.output.write(f'{usr} {val} \n')

    def load_test(self, user: int):

        path = f'{inter}/{user}'

        if os.path.exists(path):
            self.output = open(path, 'a')
            next_target = len(open(path, 'r').readlines())
        else:
            self.output = open(path, 'w')
            next_target = 0

        if not next_target:
            if os.path.exists(ifile):
                os.remove(ifile)
            if os.path.exists(ibyte):
                os.remove(ibyte)
            if os.path.exists(ihelp):
                os.remove(ihelp)

        return next_target

    def load_drive(self):

        os.system(load_helper)
        secret = open(ibyte, 'rb').read()
        public = open(ifile, 'r').read()
        return secret, json.loads(public)

    def save_drive(self, secret: bytes, public: list):

        os.system(save_helper)
        open(ibyte, 'wb').write(secret)
        open(ifile, 'w').write(str(public))

    def inter_error(self, user: int):

        data = self.module.d_list
        test = self.module.u_list
        iter = self.load_test(user)

        if self.N > len(data[user]):
            return print('not enough data')

        if iter == len(test):
            return print('already finish')

        if os.path.exists(ifile):
            u_secret, i_vector = self.load_drive()
            self.system.reliables[user] = i_vector
        else:
            u_vector = self.module.load_user_data(user, self.N)
            u_secret = self.system.enroll_user(user, u_vector)
            i_vector = self.system.reliables[user]
            self.save_drive(u_secret, list(i_vector))

        for ix in test[iter:]:
            if ix == user or self.K > len(data[ix]):
                self.update_output(ix, None)
            else:
                x_vector = self.module.load_user_data(ix, self.K)
                x_secret = self.system.verify_user(user, x_vector)
                self.update_output(ix, u_secret == x_secret)

    def intra_error(self):

        data = self.module.d_list
        test = self.module.u_list
        size = self.N + self.K

        for user in test:

            if len(data[user]) < size:
                continue

            recv = self.module.load_user_data(user, size)
            urow, vrow = recv[:self.N], recv[self.N:]
            ukey = self.system.enroll_user(user, urow)
            vkey = self.system.verify_user(user, vrow)

            print(f'{user} {ukey != vkey}')
