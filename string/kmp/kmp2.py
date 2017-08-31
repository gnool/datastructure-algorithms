# python3

class KMP:
    """KMP(text,pattern) -> find all pattern matches in text
    Atributes:
        text          Text
        pattern       Pattern
    """
    
    def __init__(self,pattern,text):
        self.text = text
        self.pattern = pattern
        
    def match(self):
        """Build the prefix function for 'pattern$text' and return the matches."""
        pattern = self.pattern+"$"+self.text
        results = []
        m = len(pattern)
        n = len(self.pattern)
        n2 = n*2
        p = [None]*m
        p[0] = 0
        k = 0
        for i in range(1,m):
            while k > 0 and pattern[i] != pattern[k]:
                k = p[k-1]
            if pattern[k] == pattern[i]:
                k = k+1
            p[i] = k
            if k == n:
                results.append(i-n2)
        return results


if __name__ == '__main__':
    kmp = KMP(input(),input())
    print(" ".join(map(str,kmp.match())))
