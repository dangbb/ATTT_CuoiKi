

class ShiftCipher:
    @staticmethod
    def encode(plaintext, key):
        result = ""

        for c in plaintext:
            result = result + chr((ord(c) - ord('A') + 26 + key) % 26 + ord('A'))
        return result

    @staticmethod
    def decode(ciphertext, key):
        result = ""

        for c in ciphertext:
            result = result + chr((ord(c) - ord('A') + 2 * 26 - key) % 26 + ord('A'))
        return result

    @staticmethod
    def analysis(ciphertext):
        for key in range(0, 26):
            print("Khóa: {}\tVăn bản giải mã: {}".format(key, ShiftCipher.decode(ciphertext, key)))


if __name__ == "__main__":
    with open("input.inp", "r") as f:
        key = int(f.readline())
        plaintext = f.readline().upper().strip('\n')

    system = ShiftCipher()
    print("Giá trị của khóa: key = ", key)
    print("Giá trị của bản rõ: ", plaintext)
    ciphertext = system.encode(plaintext, key)
    print("Giá trị bản mã: ", ciphertext)
    predicted_plaintext = system.decode(ciphertext, key)
    print("Giá trị bản rõ được mã hóa: ", predicted_plaintext)

    system.analysis(ciphertext)
