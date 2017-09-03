# python3

class SuffixArray:
    """SuffixArray(string) -> build suffix array for string.
    Attributes:
        string        input string
        sa            suffix array of input string
    """
    def __init__(self, string):
        self.string = string
        self.sa = []
        
    def _sort_char(self):
        """Sort string by counting sort."""
        n = len(self.string)
        order = [None]*n
        count = {}
        for i in self.string:
            if i not in count:
                count[i] = 0
            count[i] += 1
        for i, (c, ct) in enumerate(sorted(count.items())):
            if i > 0:
                count[c] += count[prev]
            prev = c
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

    def match(self, patterns):
        """Return all matches of patterns."""
        results = []
        string = self.string
        sa = self.sa
        for pattern in patterns:
            m = len(pattern)
            _min = 0
            _max = len(string)
            # Binary search for the lower limit
            while _min < _max:
                mid = (_min + _max) // 2
                if pattern > string[sa[mid]:sa[mid]+m]:
                    _min = mid + 1
                else:
                    _max = mid
            start = _min
            _max = len(string)
            # Binary search for the upper limit
            while _min < _max:
                mid = (_min + _max) // 2
                if pattern < string[sa[mid]:sa[mid]+m]:
                    _max = mid
                else:
                    _min = mid + 1
            end = _max
            if start <= end:
                matches = []
                for i in range(start,end):
                    matches.append(sa[i])
                results.append(matches)
        return results


if __name__ == '__main__':
    string = input() + '$'
    # Replace '$' with any character not in input string
    patterns = input().split()
    sa = SuffixArray(string)
    sa.sa = sa.build()
    matches = sa.match(patterns)
    for pattern, match in zip(patterns,matches):
        print(pattern,':',match)
