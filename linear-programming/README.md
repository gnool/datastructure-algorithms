# Overview
List of algorithms related to linear programming:
- Simplex algorithm 

# Implementation details
`simplex.py` implements the two-phase Simplex algorithm with Bland's rule. The pivoting operation is done mainly via numpy's matrix multiplication.

# Test case
An useful test case can be used to benchmark the performance of a particular implementation of Simplex algorithm.
Consider the linear program ```Ax <= b```, where the objective function is ```cx```.
Consider the test case where
```
A =
 1 0 0 0 0 . . . 0  
 2 1 0 0 0 . . . 0  
 2 2 1 0 0 . . . 0  
 2 2 2 1 0 . . . 0  
   
     . . . . .   
  
 2 2 2 . . . 2 1 0  
 2 2 2 . . . 2 2 1  
  
b =   
2^0 2^1 2^2 2^3 2^4 ... 2^(n-1)  
  
c = 
1 1 1 1 . . . . . . . . . . 1    (i.e. n 1's)
```
It turns out that the number of pivoting operations required in this test varies exponentially with n (```~1.6^n```).
