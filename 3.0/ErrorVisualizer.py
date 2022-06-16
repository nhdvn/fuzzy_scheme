
import os
from TempExtractor import VoiceTemplateLoader
from CryptoSystem import VoiceCryptoSystem


class FalseRateTester:

    def __init__(self):
        self.N = 5
        self.K = 3
        self.system = VoiceCryptoSystem()
        self.module = VoiceTemplateLoader()
        self.out = None

    def update_output(self, usr, val):

        self.out.write(f'{usr} {val} \n')

    def load_test(self, user: int):

        path = f'/content/drive/MyDrive/Inter/{user}'

        if os.path.isfile(path):
            self.out = open(path, 'a')
            progress = open(path, 'r').readlines()
            return len(progress)

        self.out = open(path, 'w')
        return 0

    def inter_error(self, user: int):

        data = self.module.dlist
        test = self.module.ulist
        iter = self.load_test(user)

        if self.N > len(data[user]):
            return print('not enough data')

        if iter == len(test):
            return print('already finish')

        udat = self.module.load_user_data(user, self.N)
        ukey = self.system.enroll_user(user, udat)

        for iv in test[iter:]:
            if iv == user:
                self.update_output(iv, None)
            else:
                vdat = self.module.load_user_data(iv, self.K)
                vkey = self.system.verify_user(user, vdat)
                self.update_output(iv, ukey == vkey)

    def intra_error(self):

        data = self.module.dlist
        test = self.module.ulist
        size = self.N + self.K

        for user in test:

            if len(data[user]) < size:
                continue

            recv = self.module.load_user_data(user, size)
            udat, vdat = recv[:self.N], recv[self.N:]
            ukey = self.system.enroll_user(user, udat)
            vkey = self.system.verify_user(user, vdat)

            print(f'{user} {ukey != vkey}')


if __name__ == "__main__":
    tmp = FalseRateTester()
    tmp.intra_error()
