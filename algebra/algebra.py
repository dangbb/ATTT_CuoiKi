import numpy as np
from dmath.dmath import *

def modNegative(val):
    return (val + (- val // 26) * 26 + 26) % 26

class ModMatrix:
    def __init__(self, np_arr: np.ndarray, calcInv=True):
        self.n = np_arr.shape[0]
        self.arr = np_arr

        if not calcInv:
            return

        det = np.linalg.det(self.arr)
        self.invArr = np.linalg.inv(self.arr) * det

        for i in range(self.n):
            for j in range(self.n):
                self.invArr[i][j] = round(self.invArr[i][j])

        self.invArr = self.invArr.astype(np.int)

        det = round(det)
        det = modNegative(det)

        print("Giá trị của định thức: ", det)

        assert det != 0, "Ma trận có giá trị định thức bằng không, không có nghịch đảo."
        assert gcd(det, 26) == 1, "Định thức không nguyên tố cùng nhau với 26."

        self.invArr = self.invArr * invModulo(det, 26)[0]

        self.arr = self.arr.tolist()
        self.invArr = self.invArr.tolist()

        for i in range(self.n):
            for j in range(self.n):
                self.invArr[i][j] = modNegative(self.invArr[i][j])

    def __len__(self):
        return self.n

    def getInv(self):
        return self.invArr

    def getArr(self):
        return self.arr

    def matmul(self, arr_1d):
        assert len(arr_1d) == self.n, "Độ dài của mạng không hợp lệ, phải bằng {}".format(self.n)
        result = np.zeros_like(arr_1d).tolist()

        for i in range(self.n):
            for j in range(self.n):
                result[i] += arr_1d[j] * self.arr[j][i]
            result[i] = result[i] % 26
        return result

    def matmulInv(self, ciphertext):
        assert len(ciphertext) == self.n, "Độ dài của mạng không hợp lệ, phải bằng {}".format(self.n)
        result = np.zeros_like(ciphertext).tolist()

        for i in range(self.n):
            for j in range(self.n):
                result[i] += ciphertext[j] * self.invArr[j][i]
            result[i] = result[i] % 26
        return result

