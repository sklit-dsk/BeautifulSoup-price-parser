import re

class Pretraga:
    def __init__(self):
        self._keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def encode(self, j):
        '''Encode search combination (multicom)'''
        if len(j) > 2:
            j += "|123"
        w = ""
        k = 0
        j = self._utf8_encode(j)
        while k < len(j):
            m = ord(j[k])
            k += 1
            q = ord(j[k]) if k < len(j) else 0
            k += 1
            l = ord(j[k]) if k < len(j) else 0
            k += 1
            v = m >> 2
            p = ((m & 3) << 4) | (q >> 4)
            x = ((q & 15) << 2) | (l >> 6)
            h = l & 63
            if k > len(j):
                h = x = 64
            elif k == len(j):
                h = 64
            w += self._keyStr[v] + self._keyStr[p] + self._keyStr[x] + self._keyStr[h]
        return w

    def _utf8_encode(self, h):
        h = h.replace("\r\n", "\n")
        k = ""
        for i in range(len(h)):
            j = ord(h[i])
            if j < 128:
                k += chr(j)
            elif 127 < j < 2048:
                k += chr((j >> 6) | 192)
                k += chr((j & 63) | 128)
            else:
                k += chr((j >> 12) | 224)
                k += chr(((j >> 6) & 63) | 128)
                k += chr((j & 63) | 128)
        return k
