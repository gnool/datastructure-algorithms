# Uses python3

def fibonacci_partial_sum_last_digit(m, n):
    '''Returns the last digit of the sum of all the Fibonacci numbers between Fm and Fn (inclusive)'''
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

    # We reshuffle the Pisano period list (since it was constructed based on F0 instead of Fm)
    new_start_index = m % period
    mod_list = mod_list[new_start_index:] + mod_list[:new_start_index]
    length = (n - m + 1)
    # Calculate how many full periods and partial period is involved
    quotient = length // period
    remainder = length % period
    # Then sum all (Fn mod m) in total
    total = sum(mod_list)*quotient + sum(mod_list[:remainder])
    # The last digit is simply total%10
    return total % 10

if __name__ == '__main__':
    m, n = map(int, input().split())
    print(fibonacci_partial_sum_last_digit(m, n))
