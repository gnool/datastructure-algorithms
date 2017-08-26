# Uses python3

def fibonacci_sum_last_digit(n):
    '''Returns the last digit of the sum of the first n Fibonacci numbers (F0 = 0, F1 = 1)'''
    # Return known results for F0 and F1
    if n <= 1:
        return n

    # First we get the Pisano period (for m = 10)
    mod_list = [0,1]
    prev = 0
    fib = 1
    while (True):
        prev, fib = fib, (prev+fib)%10
        mod_list.append(fib)
        if (fib == 0):
            period = len(mod_list)-1
            for k in range(1,period):
                prev, fib = fib, (prev+fib)%10
                mod_list.append(fib)
                if (mod_list[k] != fib):
                    break
            else:
                # We need only one period in our list
                mod_list = mod_list[:period]
                break

    # Calculate how many full periods and partial period is involved with n
    quotient = (n+1) // period
    remainder = (n+1) % period
    # Then sum all (Fn mod m) in total
    total = sum(mod_list)*quotient + sum(mod_list[:remainder])
    # The last digit is simply total%10
    return total % 10

if __name__ == '__main__':
    n = int(input())
    print(fibonacci_sum_naive(n))
