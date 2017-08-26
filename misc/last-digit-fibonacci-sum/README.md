# Overview
This algorithm returns the last digit of the sum of the first n Fibonacci numbers.
It supports efficient calculation by utilizing [Pisano period](https://en.wikipedia.org/wiki/Pisano_period) (finding Pisano period of mod 10 is extremely fast). 
Using the modular arithmetic property **(A+B) mod m = (A mod m + B mod m) mod m**, one can show that
**(A mod m + B mod m + C mod m + ...) mod m = (A + B + C + ... ) mod m**

# Note of usage
The running time of this algorithm is O(1) (as compared to O(n) if we sum up the entire Fibonacci sequence up to n).
Calculation of Pisano period for m = 10 is very fast (Pisano period of 10 is 60). If this algorithm is heavily called, one can even store the 60 integers (the Pisano period) in a list instead of calculating it everytime.
