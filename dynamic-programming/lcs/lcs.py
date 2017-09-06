#Uses python3

import numpy as np
from itertools import product

class LCS:
    def __init__(self, strings):
        self._strings = strings
        self._array = None
        self._build()

    def _build(self):
        """Bottom-up dynamic programming."""
        strings = self._strings
        n = len(strings)          
        indices = []
        lengths = []
        for string in strings:
            indices.append(range(1,len(string)+1))
            lengths.append(len(string)+1)
        lcs = np.zeros(lengths,dtype=np.uint64)
        # product(*indices) generates nested loops where the number of nest loops
        # equals len(indices).
        for index in product(*indices):
            for i, string in enumerate(strings):
                if i == 0:
                    continue
                if string[index[i]-1] != strings[i-1][index[i-1]-1]:
                    break
            else:
                index2 = tuple(np.subtract(index,(1,)*n))
                lcs[index] = lcs[index2]+1
                continue
            max_ = -1
            indices2 = []
            for i in range(n):
                indices2.append(range(index[i]-1,index[i]+1))
            # Below is another nested for loops to check all the previous neighbours
            # for the one with max lcs.
            for index2 in product(*indices2):
                if index2 == index:
                    continue
                if lcs[index2] > max_:
                    max_ = lcs[index2]
                    max_index = index2
            lcs[index] = lcs[max_index]
        self._array = lcs

    def length(self):
        """Return length of longest common subsequence."""
        n = len(self._strings)
        lengths = []
        for string in self._strings:
            lengths.append(len(string))
        lengths = tuple(lengths)
        return self._array[lengths]

    def string(self):
        """Return string of longest common subsequence."""
        n = len(self._strings)
        array = self._array
        stack = []
        results = []
        lengths = []
        for string in self._strings:
            lengths.append(len(string))
        lengths = tuple(lengths)
        cur = lengths
        # We exit this infinite loop only when one of the indices of cur becomes
        # zero, in which case there can be no further increase in string length.
        while True:
            for i in cur:
                if i == 0:
                    return "".join(results[::-1])
            else:
                for i, string in enumerate(strings):
                    if i == 0:
                        continue
                    if string[cur[i]-1] != strings[i-1][cur[i-1]-1]:
                        break
                else:
                    results.append(strings[0][cur[0]-1])
                    cur = tuple(np.subtract(cur,(1,)*n))
                    continue
                max_ = -1
                indices = []
                for i in range(n):
                    indices.append(range(cur[i]-1,cur[i]+1))
                for index in product(*indices):
                    if index == cur:
                        continue
                    if array[index] > max_:
                        max_ = array[index]
                        max_index = index
                cur = max_index


if __name__ == '__main__':
    n = int(input())
    strings = []
    for _ in range(n):
        strings.append(input())
    lcs = LCS(strings)
    print(lcs.length())
    print(lcs.string())
