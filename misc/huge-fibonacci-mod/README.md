# Overview
This algorithm returns Fn mod m, where
- Fn is the nth Fibonacci number (F0 = 0, F1 = 1)
- n and m are integers

It supports large n (as big as you want) which would be practically impossible to calculate if you start from F0 and advance all the way to Fn. To circumvent this problem we resort to a concept in number theory - [Pisano period](https://en.wikipedia.org/wiki/Pisano_period).
As soon as we find the Pisano period p, (Fn mod m) boils down to extracting the (n mod p) item in the list containing one period of (Fn mod m). To speed things up, the modular arithmetic property **(A+B) mod m = (A mod m + B mod m) mod m** is used.

# Note of usage
The bottleneck in this algorithm is really m, since the period p increases with m - which means it takes longer to find the period. Of course, if the Fn list reaches n before a period is found, the program returns Fn mod m.
