import math

class Convert(object):
    def __init__(self):
        self.chSet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.radix = 62

    def toNum(self, Str):
        n = i = len(Str) - 1
        ret = 0

        while i >= 0:
            c = Str[i]
            ret += self.chSet.index(c) * int(math.pow(self.radix, n - i))
            i -= 1
        return ret

    def toStr(self, Num):
        if Num < self.radix:
            return ""+self.chSet[Num]

        r = Num % self.radix
        d = Num // self.radix
        c = self.chSet[r]

        if d >= self.radix:
            return ""+self.toStr(d)+c
        else:
            return ""+self.chSet[d]+c

if __name__ == '__main__':
    transformer = Convert()
    print(transformer.toNum(transformer.toStr(45236)))