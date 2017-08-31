# python3

class KMP:
    """KMP(text,pattern) -> find all pattern matches in text
    Atributes:
        text          Text
        pattern       Pattern
        prefix        Prefix function for pattern
    """
    
    def __init__(self,pattern,text):
        self.pattern = pattern
        self.text = text
        self.prefix = []

    def build_prefix(self):
        """Build the prefix function for pattern."""
        pattern = self.pattern
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
        self.prefix = p
        
    def match(self):
        """Return all the pattern matches in text."""
        results = []
        pattern = self.pattern
        text = self.text
        m = len(self.pattern)
        n = len(self.text)
        p = self.prefix
        k = 0
        for i in range(n):
            while k > 0 and text[i] != pattern[k]:
                k = p[k-1]
            if pattern[k] == text[i]:
                k = k+1
            if k == m:
                results.append(i-m+1)
                k = p[k-1]
        return results


if __name__ == '__main__':
    kmp = KMP(input(),input())
    kmp.build_prefix()
    print(" ".join(map(str,kmp.match())))
