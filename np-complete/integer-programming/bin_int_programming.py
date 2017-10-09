# python3

import itertools as it

class BinaryIntegerProgramming:
    """Binary integer programming to SAT converter:

    Attributes:
        total_inequality    number of inequalities
        total_variable      number of variables
        matrix              2D list containing coefficients of matrix A
        b                   1D vector containing components of vector b

    Further details:
    Matrix A and vector b are related by Ax<=b, where x is a binary vector.
    """
    def __init__(self):
        self.total_inequality = 0
        self.total_variable = 0
        self.matrix = []
        self.b = []
        
    def read_data(self):
        """Read input:

        Format:
        Line 0: n m
        Line 1: c11 c12 c13 ... c1m
        Line 2: c21 c22 c23 ... c2m
        ...
        Line n: cn1 cn2 cn3 ... cnm
        Line n+1: b1 b2 c3 ... bn

        Explanation:
        Line 1 to n represents the matrix coefficients in A, and line n+1
        represents the components in vector b. A and b are related by Ax<=b,
        where x is the binary vector.

        n = number of inequalities
        m = number of variables
        c = coefficients in matrix A
        b = components in vector b
        """
        n, m = list(map(int, input().split()))
        self.total_inequality = n
        self.total_variable = m
        matrix = []
        for i in range(n):
            matrix += [list(map(int, input().split()))]
        b = list(map(int, input().split()))
        self.matrix = matrix
        self.b = b
        
    def print_SAT(self):
        """Output the Binary Integer Programming problem in SAT form."""
        clauses = []
        b = self.b
        m = self.matrix
        # (Ax <= b)
        for row, b in zip(m, b):
            non_zeros = [(i, coeff) for (i, coeff) in enumerate(row) if coeff != 0]
            # Check if current inequality is unsatisfiable.
            min_ = sum(coeff for i, coeff in non_zeros if coeff < 0)
            if min_ > b:
                self.print_unsatisfiable()
                return
            # Check if current inequality is satisfiable.
            max_ = sum(coeff for i, coeff in non_zeros if coeff > 0)
            if max_ <= b:
                continue
            # Otherwise find the clauses
            for p in it.product([0,1], repeat = len(non_zeros)):
                # Find the set of binary vector components that would violate the inequality.
                if sum(p[i]*non_zeros[i][1] for i in range(len(non_zeros))) > b:
                    # e.g. The violating clause representing [0, 1, 0] would be -a AND b AND -c,
                    # negating the clause would produce non-violating clause a OR -b OR c
                    # (de Morgan's law). p2 below contains the coefficients for the non-violating
                    # clause (i.e. [1 -1 1] for the example above).
                    p2 = [1 if p[i] == 0 else -1 for i in range(len(non_zeros))]
                    clauses.append([(non_zeros[i][0]+1)*p2[i] for i in range(len(non_zeros))])
        # All the clauses are satisfiable; print simple output.
        if not clauses:
            self.print_satisfiable()
        # Otherwise, not all clauses are satisfiable; proceed to print constructed clauses.
        else:
            # Print number of clauses and number of variables
            print(len(clauses), self.total_variable)
            # Print all clauses
            for clause in clauses:
                clause.append(0)
                print(" ".join(map(str,clause)))

    def print_satisfiable(self):
        """Print a set of satisfiable clauses."""
        print("1 1")
        print("1 -1 0")
        
    def print_unsatisfiable(self):
        """Print a set of unsatisfiable clauses."""
        print("2 1")
        print("1 0")
        print("-1 0")

        
if __name__ == '__main__':
    binary = BinaryIntegerProgramming()
    binary.read_data()
    binary.print_SAT()
