import string

from dmath.dmath import *
from dstring.dstring import *
from statistic.English import *
import itertools
import numpy as np
import random


class AffineCipher:

    def __init__(self, key=None):
        self.mod = 26

        if key is None:
            a = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
            self.a = a[random.randint(0, len(a) - 1)]
            self.b = random.randint(0, 26 - 1)
        else:
            assert len(key) == 2, "Giá trị khóa đầu vào không hợp lệ, phải có dạng [a, b], trong đó a nguyên tố cùng nhau với 26."
            assert gcd(26, key[0]) == 1, "Giá trị khóa đầu vào không hợp lệ, phải có dạng [a, b], trong đó a nguyên tố cùng nhau với 26."
            self.a = key[0]
            self.b = key[1]
        self.invA = invModulo(self.a, self.mod)[0]

        print("Giá trị khóa: a = {}, b = {}".format(self.a, self.b))

    def encode(self, plaintext):
        result = ''
        for c in plaintext:
            numberize_c = ord(c) - ord('A')
            new_numberize_c = (numberize_c * self.a + self.b) % self.mod

            new_c = chr(new_numberize_c + ord('A'))
            result = result + new_c
        return result

    def decode(self, ciphertext):
        result = ''
        for c in ciphertext:
            numberize_c = ord(c) - ord('A')
            new_numberize_c = (((numberize_c - self.b + self.mod) % self.mod) * self.invA) % self.mod

            new_c = chr(new_numberize_c + ord('A'))
            result = result + new_c
        return result

    @staticmethod
    def decode_static(ciphertext, a, b, mod):
        invA = invModulo(a, mod)[0]
        result = ''
        for c in ciphertext:
            numberize_c = ord(c) - ord('A')
            new_numberize_c = (((numberize_c - b + mod) % mod) * invA) % mod

            new_c = chr(new_numberize_c + ord('A'))
            result = result + new_c
        return result


    @staticmethod
    def analysis(ciphertext: str):
        mod = 26
        print("Giá trị bản mã: ")
        print(ciphertext)

        freq = Frequency()
        mono, _, _ = freq.fit(ciphertext)

        print("Ta chọn 2 chữ cái xuất hiện nhiều nhất trong bản rõ, và đặt giả thiết chúng ánh xạ tới 2 chữ cái khác trong nhóm xuất hiện nhiều nhất trong tiếng Anh.")

        print("Do 26 không phải là số nguyên tố, nên dù có chọn a là số nguyên tố, vẫn có khả năng phương trình không có nghiệm và không thể giải được.")

        freq_in_Eng = list(frequencies.keys())

        x1 = ord(freq_in_Eng[0]) - ord('A')
        x2 = ord(freq_in_Eng[1]) - ord('A')

        print("Giá trị của x1 = {} = {}, x2 = {} = {}".format(freq_in_Eng[0], x1, freq_in_Eng[1], x2))

        print("Giá trị mono: ", mono)

        for diff in range(1, 26):
            for first_letter in range(0, diff + 1):
                for second_letter in range(0, diff + 1):
                    if first_letter == second_letter:
                        continue
                    y1 = ord(mono[first_letter]) - ord('A')
                    y2 = ord(mono[second_letter]) - ord('A')

                    delta_y = (y1 - y2 + mod) % mod
                    delta_x = (x1 - x2 + mod) % mod

                    print("** Nhận được giá trị y1 = {} = {}, y2 = {} = {}".format(
                        mono[first_letter],
                        y1,
                        mono[second_letter],
                        y2
                    ))

                    gcdxy = gcd(delta_x, delta_y)
                    if gcdxy > 1:
                        delta_x = delta_x // gcdxy
                        delta_y = delta_y // gcdxy

                    if gcd(delta_x, mod) != 1:
                        print("Giá trị của delta x = {} không nguyên tố cùng nhau với 26.".format(delta_x))
                        continue
                    print("Delta y = {}, Delta x = {}, inv Delta x = {}".format(delta_y, delta_x, invModulo(delta_x, mod)[0]))
                    a = (delta_y * invModulo(delta_x, mod)[0]) % mod

                    if gcd(a, mod) != 1:
                        print("Giá trị của a = {} không nguyên tố cùng nhau với 26.".format(a))
                        continue
                    b = (y1 - (a * x1) % mod + mod) % mod
                    print("Nhận được giá trị a = {} = {}, b = {} = {}".format(
                        freq_in_Eng[first_letter],
                        a,
                        freq_in_Eng[second_letter],
                        b))
                    print("Bản rõ sau khi giải mã:")
                    print(AffineCipher.decode_static(ciphertext, a, b, mod))
                    print("Nhập 'y' nếu bản mã có nghĩa. Các ký tự khác trong trường hợp ngược lại.")

                    while True:
                        x = input()
                        if x == 'y':
                            print("Đã tìm được bản rõ phù hợp.")
                            return
                        else:
                            break



if __name__ == "__main__":
    with open("input.inp", "r") as f:
        input_string = f.read().strip(' ').strip('\n').upper()
        input_string = input_string.translate(str.maketrans('', '', string.punctuation + '\n' + ' '))

        print("Xâu đầu vào: ", input_string)

        cipher = AffineCipher([3, 15])
        ciphertext = cipher.encode(input_string)
        print("Giá trị bản mã: ")
        print(ciphertext)
        predicted_plaintext = cipher.decode(ciphertext)
        print("Giá trị bản rõ dự đoán: ")
        print(predicted_plaintext)

        print("Thám mã bản mã")
        AffineCipher.analysis(ciphertext)
