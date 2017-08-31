# python3

class Cyclic:
    """Cyclic(string1,string2) -> check if strings are cyclic rotations of each other
    Atributes:
        string1        Input string 1
        string11       (Input string 1) * 2
        string2        Input string 2
    """
    
    def __init__(self,s1,s2):
        self.string1 = s1
        self.string11 = s1*2
        self.string2 = s2

    def build_prefix(self):
        """Build the prefix function for pattern."""
        pattern = self.string2
        m = len(pattern)
        p = [None]*m
        p[0] = 0
        k = 0
        for i in range(1,m):
            while k > 0 and pattern[i] != pattern[k]:
                k = p[k-1]
            if pattern[k] == pattern[i]:
                k = k+1
            p[i] = k
        self._prefix = p
        
    def match(self):
        """Return all the pattern matches in text."""
        self.build_prefix()
        pattern = self.string2
        text = self.string11
        m = len(self.string2)
        n = len(self.string11)
        p = self._prefix
        k = 0
        for i in range(n):
            while k > 0 and text[i] != pattern[k]:
                k = p[k-1]
            if pattern[k] == text[i]:
                k = k+1
            if k == m:
                return True
        return False


if __name__ == '__main__':
    cyclic = Cyclic(input(),input())
    print(cyclic.match())
