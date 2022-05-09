import string

from dmath.dmath import *
from dstring.dstring import *
from statistic.English import *
from statistic.IndexOfCoincidence import *
from algebra.algebra import *


class HillCipher:
    def __init__(self, key):
        self.key = ModMatrix(key)
        self.n = key.shape[0]

    def encode(self, plaintext):
        while len(plaintext) % self.n != 0:
            plaintext = plaintext + 'Q'

        result = ''
        for i in range(0, len(plaintext), self.n):
            currentEncode = []
            for j in range(i, i + self.n):
                c = plaintext[j]
                currentEncode.append(ord(c) - ord('A'))

            ciphertext = self.key.matmul(np.array(currentEncode, dtype=np.int))
            for j in range(0, self.n):
                result = result + chr(ciphertext[j] + ord('A'))
        return result


    def decode(self, ciphertext):
        result = ''
        for i in range(0, len(ciphertext), self.n):
            currentEncode = []
            for j in range(i, i + self.n):
                c = ciphertext[j]
                currentEncode.append(ord(c) - ord('A'))

            plaintext = self.key.matmulInv(np.array(currentEncode, dtype=np.int))
            for j in range(0, self.n):
                result = result + chr(plaintext[j] + ord('A'))

        while len(result) > 0 and result[-1] == 'Q':
            result = result[:-1]
        return result

    @staticmethod
    def decode_static(ciphertext, key):
        n = len(key)
        result = ''
        for i in range(0, len(ciphertext), n):
            currentEncode = []
            for j in range(i, i + n):
                c = ciphertext[j]
                currentEncode.append(ord(c) - ord('A'))

            plaintext = key.matmulInv(np.array(currentEncode, dtype=np.int))
            for j in range(0, n):
                result = result + chr(plaintext[j] + ord('A'))
        return result

    @staticmethod
    def analysis(ciphertext, plaintext, n):
        print("Chọn ra m các truy vấn độ dài m liên tiếp trên bản mã và bản rõ tương ứng của chúng.")

        start_ = 0
        while True:
            try:
                print("Giá trị bắt đầu bằng ", start_)
                plain_group = []
                plainTextTaken = {}
                for i in range(start_, len(plaintext), n):
                    if len(plain_group) == n:
                        break
                    if i + n - 1 <= len(plaintext) - 1:
                        if plaintext[i: i+n] in plainTextTaken.keys():
                            continue
                        currentEncode = []
                        for j in range(i, i + n):
                            c = plaintext[j]
                            currentEncode.append(ord(c) - ord('A'))
                        plain_group.append(currentEncode)

                cipher_group = []
                cipherTextTaken = {}
                for i in range(start_, len(ciphertext), n):
                    if len(cipher_group) == n:
                        break
                    if i + n - 1 <= len(ciphertext) - 1:
                        if ciphertext[i: i+n] in cipherTextTaken.keys():
                            continue
                        currentEncode = []
                        for j in range(i, i + n):
                            c = ciphertext[j]
                            currentEncode.append(ord(c) - ord('A'))
                        cipher_group.append(currentEncode)

                print("Giá trị của plain\n", plain_group)
                print("Giá trị của cipher\n", cipher_group)

                if len(plain_group) < n or len(cipher_group) < n:
                    print("Không đủ các dãy phân biệt để thám mã")
                    return

                Invplain = ModMatrix(np.array(plain_group, dtype=np.int)).getInv()
                cipher = np.array(cipher_group, dtype=np.int)
                predict_key = np.dot(Invplain, cipher)

                for i in range(n):
                    for j in range(n):
                        predict_key[i][j] = modNegative(predict_key[i][j])

                print("Giá trị của nghịch đảo của plain\n", Invplain)
                print("Giá trị của khóa dự đoán được là\n", predict_key)
                print("Giá trị của bản mã với khóa tương ứng là\n", HillCipher.decode_static(
                    ciphertext,
                    ModMatrix(predict_key)
                ))
                break
            except Exception as e:
                print(e)
                start_ += n


if __name__ == "__main__":
    with open("input.inp", "r") as f:
        input_string = f.read().strip(' ').strip('\n').upper()
        input_string = input_string.translate(str.maketrans('', '', string.punctuation + '\n' + ' '))

        print("Xâu đầu vào: ", input_string)

        cipher = HillCipher(np.array([
            [7, 19],
            [6, 3]
        ]))
        ciphertext = cipher.encode(input_string)
        print("Giá trị bản mã: ", ciphertext)
        predict_plaintext = cipher.decode(ciphertext)
        print("Giá trị bản rõ:", predict_plaintext)

        print("Tiến hành thám mã giá trị của khóa\n")
        HillCipher.analysis(ciphertext, predict_plaintext, 2)