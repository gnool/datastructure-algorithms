# python3

class BurrowsWheeler:
    """Burrows-Wheeler transform and string matching."""
    def __init__(self):
        self.string = None
        self.charset = {'$':0,'A':1,'C':2,'G':3,'T':4}
        self.ranks = None
        self.first_occ = None

    def transform(self, string):
        """Perform Burrows-Wheeler transform on input string."""
        sa = SuffixArray(string)
        sa = sa.build()
        bwt = []
        for i in sa:
            bwt.append(string[i-1])
        return sa, "".join(bwt)

    def invert(self, string):
        """Invert a Burrows-Wheeler transform."""
        bwt = string
        ranks, total = self._rank(bwt)
        first = self._first_occ(total)
        i = 0
        string = '$'
        while bwt[i] != '$':
            c = bwt[i]
            string += c
            i = first[c][0] + ranks[i]
        return string[::-1]

    def _rank(self, string):
        total = {}
        ranks = []
        for c in string:
            if c not in total:
                total[c] = 0
            ranks.append(total[c])
            total[c] += 1
        return ranks, total

    def _rank_all(self, string):
        total = {}
        ranks = {}
        for c, _ in self.charset.items():
            total[c] = 0
            ranks[c] = [0]
        for c in string:
            total[c] += 1
            for c, _ in total.items():
                ranks[c].append(total[c])
        return ranks, total

    def _first_occ(self, total):
        first = {}
        count = 0
        for c, t in sorted(total.items()):
            first[c] = (count, count+t)
            count += t
        return first

    def preprocess(self, string):
        """Preprocess a string."""
        self.sa, string = self.transform(string)
        self.string = string
        self.ranks, total = self._rank_all(string)
        #print(self.ranks)
        #print(self.total)
        self.first_occ = self._first_occ(total)
        #print(self.first_occ)

    def match(self, patterns):
        """Match patterns to the preprocessed string."""
        string = self.string
        n = len(string)
        results = []
        for pattern in patterns:
            top = 0
            btm = n-1
            for c in reversed(pattern):
                if top > btm:
                    break
                top = self.first_occ[c][0] + self.ranks[c][top]
                btm = self.first_occ[c][0] + self.ranks[c][btm+1] - 1
            results.append([self.sa[i] for i in range(top, btm+1)])
            #results.append(btm-top+1)
        return results


class SuffixArray:
    """SuffixArray(string) -> build suffix array for string.
    Attributes:
        string        input string
    """
    def __init__(self, string):
        self.string = string
        
    def _sort_char(self):
        """Sort string by counting sort."""
        n = len(self.string)
        order = [None]*n
        count = {}
        for i in self.string:
            if i in count:
                count[i] += 1
            else:
                count[i] = 1
        charset = [c for c in count]
        charset.sort()
        for i, c in enumerate(charset[1:]):
            count[c] += count[charset[i]]
        for i in range(n-1,-1,-1):
            char = self.string[i]
            count[char] -= 1
            order[count[char]] = i
        return order

    def _calc_char_class(self, order):
        """Calculate the equivalence class."""
        _class = [None]*len(self.string)
        _class[order[0]] = 0
        for i in range(1,len(self.string)):
            if self.string[order[i]] != self.string[order[i-1]]:
                _class[order[i]] = _class[order[i-1]] + 1
            else:
                _class[order[i]] = _class[order[i-1]]
        return _class

    def _sort_doubled(self, L, order, _class):
        """Sort doubled suffix by counting sort."""
        n = len(self.string)
        count = [0]*n
        new_order = [None]*n
        for i in range(n):
            count[_class[i]] = count[_class[i]] + 1
        for i in range(1,n):
            count[i] += count[i-1]
        for i in range(n-1,-1,-1):
            start = (order[i] - L + n) % n
            c = _class[start]
            count[c] -= 1
            new_order[count[c]] = start
        return new_order

    def _update_class(self, L, order, _class):
        """Update the equivalence class."""
        n = len(self.string)
        new_class = [None]*n
        new_class[order[0]] = 0
        for i in range(1,n):
            current = order[i]
            previous = order[i-1]
            mid_current = (current + L) % n
            mid_previous = (previous + L) % n
            if _class[current] != _class[previous] or _class[mid_current] != _class[mid_previous]:
                new_class[current] = new_class[previous] + 1
            else:
                new_class[current] = new_class[previous]
        return new_class

    def build(self):
        """Build suffix array."""
        n = len(self.string)
        order = self._sort_char()
        _class = self._calc_char_class(order)
        L = 1
        while L < n:
            order = self._sort_doubled(L,order,_class)
            _class = self._update_class(L,order,_class)
            L *= 2
        return order


if __name__ == '__main__':
    # Input format:
    # Line 1: input string
    # Line 2: number of patterns (int)
    # Line 3: all the patterns
    string = input()
    n = int(input())
    patterns = input().split()
    bw = BurrowsWheeler()
    bw.preprocess(string)
    matches = bw.match(patterns)
