
import os
from TempExtractor import VoiceTemplateLoader
from CryptoSystem import VoiceCryptoSystem


class ColabTester:

    module = VoiceTemplateLoader()
    system = VoiceCryptoSystem(512)    


    def __init__(self):
        self.N = 5
        self.K = 3
        self.file = None


    def load_tests(self, user: int):

        path = f'/content/drive/MyDrive/Inter/{user}'

        if os.path.isfile(path):
            self.file = open(path, 'a')
            test_done = open(path, 'r').readlines()
            return len(test_done)

        self.file = open(path, 'w')
        return 0


    def update_file(self, iv, val = None):

        self.file.write(f'{iv} {val}\n')


    def count_false_rate(self, user: int):

        data = self.module.dlist
        test = self.module.ulist
        iter = self.load_tests(user)

        if self.N > len(data[user]):
            return print('not enough data')

        if iter == len(test):
            return print('already finish')

        udata = self.module.load_user_data(user, 5)
        upkey = self.system.enroll_user(user, udata)

        for iv in test[iter:]:
            if iv == user:
                self.update_file(user)
            else:
                vdata = self.module.load_user_data(iv, 3)
                vpkey = self.system.verify_user(user, vdata)
                self.update_file(iv, upkey == vpkey)
