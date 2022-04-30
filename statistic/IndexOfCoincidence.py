from statistic.English import *

def IndexOfCoincidence(freq):
    ic = 0
    n = 0
    print(freq)
    for i in range(0, 26):
        n = n + freq[i]

        ic = ic + freq[i] * (freq[i] - 1)
    print(n)
    return ic / (n * (n - 1))


def ShiftQuantity(freq, g, n_):
    mg = 0
    for i in range(0, 26):
        mg = mg + frequencies[chr(i + ord('A'))] * freq[(i + g) % 26]
    return mg/n_
