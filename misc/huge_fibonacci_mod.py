# Uses python3

def get_fibonacci_huge(n, m):
    '''Returns Fn mod m (supports large n)'''
    
    # For the obvious case of F0 and F1.
    if (n <= 1):
        return n
    # Keeps a list of Fn mod m
    mod_list = [0,1]
    prev = 0         # previous F
    fib = 1          # current F
    i = 2            # number of items in list
    
    # This loop is alive until we find the Pisano period,
    # from which we can construct Fn mod m.
    while (True):
        # Advances one step forward in Fibonacci sequence
        prev, fib = fib, (prev+fib)%m
        # If it turns out we reached i = n before Pisano
        # period is found, we can just return fib.
        if (i == n):
            return fib
        i += 1
        mod_list.append(fib)
        # We note that Pisano period always starts with 0,
        # so here we check whether a period has been found.
        if (fib == 0):
            period = len(mod_list)-1
            # To check whether we have a period we advance
            # len(mod_list)-1 steps forward to see if the
            # same sequence can be repeated.
            for k in range(1,period):
                prev, fib = fib, (prev+fib)%m
                if (i == n):
                    return fib
                i += 1
                mod_list.append(fib)
                # If comparison fails, this is not a period.
                if (mod_list[k] != fib):
                    break
            # Otherwise this is indeed a period.
            else:
                return mod_list[n % period]

if __name__ == '__main__':
    n, m = map(int, input().split())
    print(get_fibonacci_huge(n, m))
