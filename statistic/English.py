import numpy as np

frequencies = {
    'E': 12.51,
    'T': 9.25,
    'A': 8.04,
    'O': 7.60,
    'I': 7.26,
    'N': 7.09,
    'S': 6.54,
    'R': 6.12,
    'H': 5.49,
    'L': 4.14,
    'D': 3.99,
    'C': 3.06,
    'U': 2.71,
    'M': 2.53,
    'F': 2.30,
    'P': 2.00,
    'G': 1.96,
    'W': 1.92,
    'Y': 1.73,
    'B': 1.54,
    'V': 0.99,
    'K': 0.67,
    'X': 0.19,
    'J': 0.16,
    'Q': 0.11,
    'Z': 0.09
}

common_digraphs = [
    'TH',
    'HE',
    'AN',
    'IN',
    'ER',
    'ON',
    'RE',
    'ED',
    'ND',
    'HA',
    'AT',
    'EN',
    'ES',
    'OF',
    'NT',
    'EA',
    'TI',
    'TO',
    'IO',
    'LE',
    'IS',
    'OU',
    'AR',
    'AS',
    'DE',
    'RT',
    'VE'
]

common_trigraphs = [
    'THE',
    'AND',
    'THA',
    'ENT',
    'ION',
    'TIO',
    'FOR',
    'NDE',
    'HAS',
    'NCE',
    'TIS',
    'OFT',
    'MEN'
]


class Frequency:
    def __init__(self):
        self.freq = {}
        self.di_freq = {}
        self.tri_freq = {}

    def get_freq(self):
        return self.freq

    def fit(self, str):
        for c in str:
            if c == ' ':
                continue
            if c.islower():
                # không xét các ký tự hay nhóm kí tự không viết hóa
                continue
            if c not in self.freq.keys():
                self.freq[c] = 0

            self.freq[c] += 1
        for i, _ in enumerate(str):
            if _ == ' ':
                continue
            if i < len(str) - 1:
                if str[i + 1] == ' ':
                    continue
                if not str[i:i + 2].islower():
                    if str[i:i+2] not in self.di_freq.keys():
                        self.di_freq[str[i:i+2]] = 0

                    self.di_freq[str[i:i+2]] += 1
                    
            if i < len(str) - 2:
                if str[i + 2] == ' ':
                    continue
                if not str[i:i + 3].islower():
                    if str[i:i+3] not in self.tri_freq.keys():
                        self.tri_freq[str[i:i+3]] = 0

                    self.tri_freq[str[i:i+3]] += 1

        sorted_mono_key = sorted(self.freq.keys(), key=lambda x: self.freq[x], reverse=True)
        sorted_di_key = sorted(self.di_freq.keys(), key=lambda x: self.di_freq[x], reverse=True)
        sorted_tri_key = sorted(self.tri_freq.keys(), key=lambda x: self.tri_freq[x], reverse=True)

        return sorted_mono_key, sorted_di_key, sorted_tri_key

    def __getitem__(self, item):
        if len(item) == 1:
            return self.freq[item]
        elif len(item) == 2:
            return self.di_freq[item]
        elif len(item) == 3:
            return self.tri_freq[item]
        else:
            raise Exception("Unsupported len = ", len(item))



