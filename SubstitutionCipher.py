import string

from dmath.dmath import *
from dstring.dstring import *
from statistic.English import *
import itertools
import numpy as np


class SubstitutionCipher:

    def __init__(self, key=None):
        if key is None:
            alphabet = np.array(range(0, 26), dtype=np.int)
            np.random.shuffle(alphabet)
            self.key = {}

            for i, value in enumerate(alphabet.tolist()):
                self.key[chr(ord('A') + i)] = chr(ord('A') + value)
        else:
            self.key = key
        self.invKey = {}

        for key in self.key.keys():
            self.invKey[self.key[key]] = key

        print("Khóa:")
        for key in self.key.keys():
            print("{} -> {}".format(key, self.key[key]))

    def encode(self, plaintext):
        result = ""
        for c in plaintext:
            if c == ' ':
                result = result + ' '
            else:
                result = result + self.key[c]
        return result

    def decode(self, ciphertext):
        result = ""
        for c in ciphertext:
            if c == ' ':
                result = result + ' '
            else:
                result = result + self.invKey[c]
        return result

    @staticmethod
    def analysis(ciphertext: str):
        print("Giá trị bản mã: ")
        print(ciphertext)
        mono_remain = list(frequencies.keys())
        mapping_from_plain_to_cipher = {}  # lowerbound input
        mapping_from_cipher_to_plain = {}  # upperbound input

        while True:
            freq = Frequency()
            mono, di, tri = freq.fit(ciphertext)

            # find tri gram and replace
            print("10 giá trị tần số xuất hiện nhiều nhất trong bản mã: ")
            limit = min(len(mono), 10)
            print(mono[:limit])
            limit = min(len(di), 14)
            print(di[:limit])
            limit = min(len(tri), 20)
            print(tri[:limit])

            print("Các chữ cái xếp theo tần suất xuất hiện nhiều nhất trong tiếng Anh chưa được sử dụng: ")
            count = 0
            for c in mono_remain:
                c = c.lower()
                if c not in mapping_from_plain_to_cipher.keys() or mapping_from_plain_to_cipher[c] is None:
                    print(c.lower(), end=" ")
                    count = count + 1
            print()

            if count == 0:
                print("Các chữ cái đã được gán hết !!")

            print("Các chữ cái thường đi đôi với nhau: ")
            s = ['SS', 'EE', 'TT', 'OO', 'FF']
            print(s)

            # Set value of the most frequencing letter to S
            # bug: do giá trị có thể bị thay đổi :<
            # cần tạo 1 hàm for riêng

            stop = False

            cipher_char = 'query[0]'
            plain_char = 'query[1]'

            while True:
                try:
                    query = str(input())
                    if query == 'stop':
                        stop = True
                        break
                    query = query.split()
                    assert len(query) == 2, "Dạng của truy vấn không hợp lệ, chỉ được có 2 thành phần"

                    cipher_char = query[0]
                    plain_char = query[1]

                    assert cipher_char.isupper(), "Dạng của truy vấn không hợp lệ, kí tự đầu phải viết hoa"
                    assert plain_char.islower(), "Dạng của truy vấn không hợp lệ, kí tự sau phải viết thường"
                    break
                except Exception as e:
                    print(e)
                    print(
                        "Xin hãy truy vấn lại theo dạng 'X x', trong đó, X là ký tự trong bản mã, x là ký tự trong bản rõ. Hoặc 'stop' để dừng.")

            if stop:
                break

            if plain_char in mapping_from_plain_to_cipher.keys():
                if mapping_from_plain_to_cipher[plain_char] is not None:
                    ciphertext = ciphertext.replace(plain_char, mapping_from_plain_to_cipher[plain_char])

            if cipher_char in mapping_from_cipher_to_plain.keys():
                if mapping_from_cipher_to_plain[cipher_char] is not None:
                    ciphertext = ciphertext.replace(mapping_from_cipher_to_plain[cipher_char], cipher_char)

            ciphertext = ciphertext.replace(cipher_char, plain_char)

            if plain_char in mapping_from_plain_to_cipher.keys():
                if mapping_from_plain_to_cipher[plain_char] is not None:
                    print("Bỏ gán {} cho {}".format(plain_char, mapping_from_plain_to_cipher[plain_char]))
                    mapping_from_cipher_to_plain[mapping_from_plain_to_cipher[plain_char]] = None

            if cipher_char in mapping_from_cipher_to_plain.keys():
                if mapping_from_cipher_to_plain[cipher_char] is not None:
                    print("Bỏ gán {} cho {}".format(mapping_from_cipher_to_plain[cipher_char], cipher_char))
                    mapping_from_plain_to_cipher[mapping_from_cipher_to_plain[cipher_char]] = None

            mapping_from_plain_to_cipher[plain_char] = cipher_char
            print("Gán {} cho {}".format(plain_char, cipher_char))
            mapping_from_cipher_to_plain[cipher_char] = plain_char

            print("Giá trị của bản mã đang giải mã: ")
            print(ciphertext)

        print("Xâu sau khi thám mã: ", ciphertext)


if __name__ == "__main__":
    with open("input.inp", "r") as f:
        input_string = f.read().strip(' ').strip('\n').upper()
        input_string = input_string.translate(str.maketrans('', '', string.punctuation + '\n'))

        print("Xâu đầu vào: ", input_string)

        cipher = SubstitutionCipher()
        cipher_string = cipher.encode(input_string)
        print("Mã hóa xâu: ", cipher_string)
        predicted_plaintext = cipher.decode(cipher_string)
        print("Giải mã xâu: ", predicted_plaintext)

        print("Thám mã: ")
        SubstitutionCipher.analysis(cipher_string)
