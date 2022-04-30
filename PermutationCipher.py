import string

from dmath.dmath import *
from dstring.dstring import *
from statistic.English import *
import itertools
import numpy as np
import random
from itertools import permutations


class PermutationCipher:

    def __init__(self, key):
        self.key = key
        self.invKey = {}
        for i in range(len(key)):
            self.invKey[self.key[i]] = i
        self.m = len(key)

    def encode(self, plaintext):
        while len(plaintext) % self.m != 0:
            plaintext = plaintext + 'Q'
        result = ''
        for i in range(0, len(plaintext), self.m):
            subtext = plaintext[i: i+self.m]
            subresult = ''
            for j in range(0, self.m):
                subresult = subresult + subtext[self.key[j]]
            result = result + subresult

        return result

    def decode(self, ciphertext):
        assert len(ciphertext) % self.m == 0, "Độ dài bản mã không chia hết cho độ dài khóa."

        result = ''
        for i in range(0, len(ciphertext), self.m):
            subtext = ciphertext[i: i+self.m]
            subresult = ''
            for j in range(0, self.m):
                subresult = subresult + subtext[self.invKey[j]]
            result = result + subresult

        return result

    @staticmethod
    def decode_static(ciphertext, invKey):
        m = len(invKey)
        assert len(ciphertext) % m == 0, "Độ dài bản mã không chia hết cho độ dài khóa."

        result = ''
        for i in range(0, len(ciphertext), m):
            subtext = ciphertext[i: i+m]
            subresult = ''
            for j in range(0, m):
                subresult = subresult + subtext[invKey[j]]
            result = result + subresult

        return result


    @staticmethod
    def analysis(ciphertext: str):
        for predictedLen in range(2, 7):
            print("Xét các hoán vị có độ dài ", predictedLen)

            l = list(permutations(range(0, predictedLen)))
            if len(ciphertext) % predictedLen != 0:
                print("Độ dài bản mã không chia hết cho độ dài khóa.")
                continue
            for permutation in l:
                permutation = list(permutation)
                print("Giá trị bản mã dự đoán: ")
                print(PermutationCipher.decode_static(ciphertext, permutation))
                print("Nếu bản mã có nghĩa, nhập 'y'. Nếu không nhập các ký tự khác.")
                isOK = input()

                if isOK == 'y':
                    return





if __name__ == "__main__":
    with open("input.inp", "r") as f:
        input_string = f.read().strip(' ').strip('\n').upper()
        input_string = input_string.translate(str.maketrans('', '', string.punctuation + '\n' + ' '))

        print("Xâu đầu vào: ", input_string)
        cipher = PermutationCipher([2, 4, 0, 5, 3, 1])

        ciphertext = cipher.encode(input_string)
        print("Giá trị bản mã\n", ciphertext)
        predicted_plaintext = cipher.decode(ciphertext)
        print("Giá trị bản rõ dự đoán\n", predicted_plaintext)
        print("Giá trị bản rõ dự đoán khi bỏ padding\n", predicted_plaintext.rstrip('Q'))

        PermutationCipher.analysis(ciphertext)
