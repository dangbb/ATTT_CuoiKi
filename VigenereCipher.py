import string

from dmath.dmath import *
from dstring.dstring import *
from statistic.English import *
from statistic.IndexOfCoincidence import *


class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def encode(self, plaintext):
        result = ''
        pos = 0
        for c in plaintext:
            new_chr_index = (ord(c) + ord(self.key[pos]) - 2 * ord('A')) % 26
            result = result + chr(new_chr_index + ord('A'))
            pos = pos + 1
            if pos == len(self.key):
                pos = 0
        return result

    def decode(self, ciphertext):
        result = ''
        pos = 0
        for c in ciphertext:
            new_chr_index = (ord(c) - ord(self.key[pos]) + 26) % 26
            result = result + chr(new_chr_index + ord('A'))
            pos = pos + 1
            if pos == len(self.key):
                pos = 0
        return result

    @staticmethod
    def decode_static(ciphertext, key):
        result = ''
        pos = 0
        for c in ciphertext:
            new_chr_index = (ord(c) - ord(key[pos]) + 26) % 26
            result = result + chr(new_chr_index + ord('A'))
            pos = pos + 1
            if pos == len(key):
                pos = 0
        return result

    @staticmethod
    def analysis(ciphertext):
        n = len(ciphertext)
        for predictLen in range(1, 10):
            print("Xét giá trị độ dài: ", predictLen)

            for startPosition in range(0, predictLen):
                freq = {}
                for i in range(0, 26):
                    freq[i] = 0

                for currentPosition in range(startPosition, n, predictLen):
                    freq[ord(ciphertext[currentPosition]) - ord('A')] += 1

                print("{:.3f}".format(IndexOfCoincidence(freq)), end = " ")
            print()

        print("Nhập giá trị độ dài muốn chọn: ", end = " ")
        targetLen = int(input())

        print("Tìm khóa với độ dài ", targetLen)
        predicted_key = ''
        for startPosition in range(0, targetLen):
            freq = {}
            for i in range(0, 26):
                freq[i] = 0
            n_ = 0

            for currentPosition in range(startPosition, n, targetLen):
                freq[ord(ciphertext[currentPosition]) - ord('A')] += 1
                n_ += 1

            cmax = -1
            letter = -1
            for currentLetter in range(0, 26):
                shiftQuantity = ShiftQuantity(freq, currentLetter, n_)
                if shiftQuantity > cmax:
                    cmax = shiftQuantity
                    letter = currentLetter

            predicted_key += chr(letter + ord('A'))
        print("Giá trị dự đoán của khóa: ", predicted_key)
        print("Giá trị dự đoán của bản rõ: ")
        print(VigenereCipher.decode_static(ciphertext, predicted_key))



if __name__ == "__main__":
    with open("input.inp", "r") as f:
        input_string = f.read().strip(' ').strip('\n').upper()
        input_string = input_string.translate(str.maketrans('', '', string.punctuation + '\n' + ' '))

        print("Xâu đầu vào: ", input_string)

        cipher = VigenereCipher('MXE')
        ciphertext = cipher.encode(input_string)
        print("Giá trị bản mã: ")
        print(ciphertext)
        predicted_plaintext = cipher.decode(ciphertext)
        print("Giá trị bản rõ dự đoán: ")
        print(predicted_plaintext)

        print("Thám mã bản mã")
        VigenereCipher.analysis(ciphertext)