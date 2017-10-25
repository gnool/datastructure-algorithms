# python 3

# Problem description:
# Given a set of error-free reads with fixed length, how do we
# assemble the original genome?
#
# One approach is to construct an overlap graph, where reads are
# represented by nodes, while an edge from read u to read v with
# weight w indicates that the suffix of read u and prefix of read
# v overlap with total length w.
#
# Once the overlap graph is constructed, the original genome can
# be reconstructed by finding the shortest Hamiltonian path through
# the graph. To avoid solving an intractable problem, we approximate
# this problem using the greedy approach: at each iteration we find
# the largest weight edge, and concatenate the corresponding two reads.
# We continue until there is no edge left - if there are still
# unconnected components in the graph, we simply concatenate them all.
#
# Note: the approach in this work involves only error-free reads
# (i.e. exact pattern matching).

# In order to perform fast pair-wise suffix-prefix max ovelap search,
# we first construct the suffix array of length (LENGTH+1) on the
# concatenated string (READ1 + $ + READ2 + $ + READ3 + ... + $) which
# consists of all reads terminated by '$'. We then march each read
# through this suffix array, and a suffix-prefix match is found whenever
# we encounter a '$' sign during this march.

# The running time of the suffix array construction is O(n * log L), where
# L is the read length and n is the total length of all the reads.
# On the other hand the matching of all the reads takes O(n * log n).

READS_NUM = 1618 # total input reads
MIN_OVERLAP = 12 # minimum suffix-prefix overlap
LENGTH = 100     # length of each read

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

    def build(self, max_length):
        """Build suffix array up to defined max length."""
        n = len(self.string)
        order = self._sort_char()
        _class = self._calc_char_class(order)
        L = 1
        while L < max_length:
            order = self._sort_doubled(L,order,_class)
            _class = self._update_class(L,order,_class)
            L *= 2
        return order

    def match(self, pattern):
        """Return all matches of patterns."""
        overlaps = {}
        string = self.string
        sa = self.sa
        _min = 0
        _max = len(string)
        start = 0
        end = len(string)
        old_start = len(string)
        for ci, c in enumerate(pattern):
            # Binary search for the lower limit
            if start == end:
                break
            _min = start
            _max = end
            while _min < _max:
                mid = (_min + _max) // 2
                if c > string[sa[mid]+ci:sa[mid]+ci+1]:
                    _min = mid + 1
                else:
                    _max = mid
            start = _min
            _max = end
            # Binary search for the upper limit
            while _min < _max:
                mid = (_min + _max) // 2
                if c < string[sa[mid]+ci:sa[mid]+ci+1]:
                    _max = mid
                else:
                    _min = mid + 1
            end = _max
            if start > old_start:
                for i in range(old_start, start):
                    if string[sa[old_start]+ci:sa[old_start]+ci+1] == '$':
                        if ci not in overlaps:
                            overlaps[ci] = set([sa[i]])
                        else:
                            overlaps[ci].add(sa[i])
                    break
            old_start = start
        return overlaps


class DisjointSet:
    """Disjoint data set (union by rank + path compression)"""
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, i):
        if i != self.parent[i]:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, a, b):
        i = self.find(a)
        j = self.find(b)
        parent = self.parent
        rank = self.rank
        if i == j:
            return
        if rank[i] > rank[j]:
            parent[j] = i
        else:
            parent[i] = j
            if rank[i] == rank[j]:
                rank[j] += 1


def construct_overlap_graph(reads):
    """Construct the overlap graph for reads."""
    edges = []
    long_string = ''
    m = len(reads[0]) + 1 # len of one read plus '$'
    for read in reads:
        long_string += read
        long_string += '$'
    sa = SuffixArray(long_string)
    sa.sa = sa.build(LENGTH + 1)
    for v, read in enumerate(reads):
        overlaps = sa.match(read)
        for w in overlaps:
            if w >= MIN_OVERLAP:
                for u in overlaps[w]:
                    edges.append((u//m, v, w))
    edges.sort(key = lambda x: x[2], reverse=True)
    return edges


def assemble_genome(edges, reads):
    """Assemble genome based on overlap graph (using greedy approach)."""
    from_ = {}
    to_ = {}
    dset = DisjointSet(len(reads))
    for u, v, w in edges:
        if u in from_:
            continue
        if v in to_:
            continue
        # Skip if this creates a cycle.
        if dset.find(u) == dset.find(v):
            continue
        dset.union(u, v)
        from_[u] = (v, w)
        to_[v] = (u, w)
    visited = set()
    genome = ""
    for i in range(len(reads)):
        if i in visited:
            continue
        current = i
        # Go back to beginning of path
        while True:
            if current not in to_:
                break
            current = to_[current][0]
        #print("Begin",current)
        # Concatenates all strings in this path
        visited.add(current)
        genome += reads[current]
        while True:
            #print("Current",current)
            if current not in from_:
                break
            v, w = from_[current]
            genome += reads[v][w:]
            visited.add(v)
            current = v
    return shortern_genome(genome)


def shortern_genome(genome):
    """Shorten genome if first and last read overlap."""
    for i in range(LENGTH, 0, -1):
        if genome[:i] == genome[-i:]:
            return genome[i:]
    return genome


if __name__ == '__main__':
    # Input will ask for READS_NUM of reads of length LENGTH.
    # The overlap graph will be constructed based on reads with
    # minimum overlap MIN_OVERLAP.
    reads = set()
    for i in range(READS_NUM):
        reads.add(input())
    reads = list(reads)
    edges = construct_overlap_graph(reads)
    genome = assemble_genome(edges, reads)
    print(genome)
