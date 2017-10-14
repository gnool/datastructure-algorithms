# python3

import numpy as np

class Simplex:
    """Simplex algorithm implementation with Bland's rule.

    Attributes:
        var        number of variables
        ineq       number of inequalities
        zero       machine epsilon (feel free to change this value)
    """
    def __init__(self, n, m):
        self.var = m
        self.ineq = n
        self.zero = 10**-9

    def init_simplex(self, tableau):
        """Phase one of Simplex algorithm: finding the right basic solution."""
        m = self.var
        n = self.ineq
        zero = self.zero
        # Check if any b value is negative.
        min_b = np.argmin(tableau[1:,0])
        if tableau[min_b+1][0] >= 0:
            # Create basic (B) and non-basic (N) sets.
            N = {i for i in range(m)}
            B = {i for i in range(m, n+m)}
            pos = [i+1 for i in range(m)] + [i+1 for i in range(n)]
            return (tableau, pos, N, B)
        # If yes, we add auxiliary variable x and change objective function to -x.
        obj = np.copy(tableau[0]) # keep a copy of the original objective functionx
        tableau[0] = 0
        append = [-1 if i == 0 else 1 for i in range(n+1)]
        append = [append[i:i+1] for i in range(n+1)]
        tableau = np.append(tableau, append, axis=1)
        # Create basic (B) and non-basic (N) sets.
        N = {i for i in range(m)}
        B = {i for i in range(m, n+m)}
        N.add(n+m) # variable subscript n+m will be our auxiliary variable
        # pos keeps track of where to find a variable in the tableau.
        # i.e. which column (row) for non-basic (basic) variable
        pos = [i+1 for i in range(m)] + [i+1 for i in range(n)] + [m+1]
        self.pivot(tableau, pos, N, B, min_b+m, n+m) # make auxiliary variable basic
        # Find optimal objective value for the auxiliary linear program.
        vec = None
        while True:
            min_ = float('inf')
            for j in N:
                if tableau[0][pos[j]] > zero:
                    # Bland's rule: get the smallest index j.
                    if j < min_:
                        min_ = j
            if min_ == float('inf'):
                break
            j = min_
            min_ = (float('inf'), None)
            col = tableau[:, pos[j]]
            col2 = tableau[:, 0]
            for i in B:
                if col[pos[i]] < -zero:
                    vec = abs(col2[pos[i]] / col[pos[i]])
                else:
                    continue
                # Bland's rule: get smaller index if there is a tie.
                if abs(vec-min_[0]) < zero:
                    if i < min_[1]:
                        min_ = (vec, i)
                elif vec < min_[0]:
                    min_ = (vec, i)
            if min_[1] == None:
                return 'Infinity'
            else:
                self.pivot(tableau, pos, N, B, min_[1], j)
            # Exit if objective value is already zero.
            if tableau[0][0] > -zero and tableau[0][0] < zero:
                break
        # Check if this auxiliary linear program can be solved.
        if tableau[0][0] > -zero and tableau[0][0] < zero:
            # Check if auxiliary variable is in basic set. If yes, move to non-basic set.
            if n+m in B:
                for i, j in enumerate(tableau[pos[n+m],1:]):
                    # Ensure that the entering variable has no zero coefficient.
                    if abs(j) > zero:
                        # Get subscript of this entering variable.
                        for k in range(n+m):
                            if pos[k] == i+1 and k in N:
                                self.pivot(tableau, pos, N, B, n+m, k)
                                break
                        break
            # Remove auxiliary variable.
            N.remove(n+m)
            tableau = np.delete(tableau, pos[n+m], 1)
            temp = pos[n+m]
            for i in N:
                if pos[i] > temp:
                    pos[i] -= 1
            pos = pos[:-1]
            # pos2 tells us which variable sits in a particular column of tableau.
            pos2 = [None]*(m+1)
            for i in N:
                pos2[pos[i]] = i
            tableau[0] = 0
            tableau[0][0] = obj[0]
            # Recall that the original m non-basic variables are 0, 1, ... m-1.
            for i in range(m):
                if i in N:
                    tableau[0][pos[i]] += obj[i+1]
                else:
                    tableau[0] += tableau[pos[i]] * obj[i+1]
            return (tableau, pos, N, B)
        else:
            # Check if auxiliary variable is in basic set. If yes, move to non-basic set.
            if n+m in B:
                for i, j in enumerate(tableau[pos[n+m],1:]):
                    # Ensure that the entering variable has no zero coefficient.
                    if j != 0:
                        # Get subscript of this entering variable.
                        for k in range(n+m):
                            if pos[k] == i+1 and k in N:
                                self.pivot(tableau, pos, N, B, n+m, k)
                                break
                        break
            for i in tableau[1:,0]:
                if i < 0:
                    return 'No solution'
            return 'Infinity'
        
        
    def solve(self, tableau):
        """Phase 2 of Simplex algorithm: finding the optimal solution."""
        m = self.var
        n = self.ineq
        zero = self.zero
        # Initiate phase one of simplex algorithm.
        init = self.init_simplex(tableau)
        if init == "No solution":
            return "No solution"
        elif init == "Infinity":
            return "Infinity"
        (tableau, pos, N, B) = init
        vec = None
        # Find optimal solution.
        while True:
            min_ = float('inf')
            for j in N:
                if tableau[0][pos[j]] > zero:
                    if j < min_:
                        min_ = j
            if min_ == float('inf'):
                break
            j = min_
            min_ = (float('inf'), None)
            col = tableau[:, pos[j]]
            col2 = tableau[:, 0]
            for i in B:
                if col[pos[i]] < -zero:
                    vec = abs(col2[pos[i]] / col[pos[i]])
                else:
                    continue
                if abs(vec-min_[0]) < zero:
                    if i < min_[1]:
                        min_ = (vec, i)
                elif vec < min_[0]:
                    min_ = (vec, i)
            if min_[1] == None:
                return 'Infinity'
            else:
                self.pivot(tableau, pos, N, B, min_[1], j)
        # Optimal solution found.
        x = [None]*m
        for i in range(m):
            if i in B:
                x[i] = tableau[pos[i]][0]
            else:
                x[i] = 0
        return x

    def pivot(self, tableau, pos, N, B, leave, enter):
        """Perform pivoting operation
           (i.e. swapping a pair of basic/non-basic variables.)
        """
        L, E = pos[leave], pos[enter]
        div = -tableau[L][E]
        tableau[L][E] = -1
        x = tableau[L] / div
        a = np.copy(tableau[:,E])
        a[L] = 0
        tableau[:,E] = 0
        tableau += np.outer(a, x)
        tableau[L] = x
        pos[leave], pos[enter] = E, L
        # Relocate entering variable to the basic set
        N.remove(enter)
        B.add(enter)
        # Relocate leaving variable to the non-basic set
        B.remove(leave)
        N.add(leave)


if __name__ == '__main__':
    # Input format
    # Line 0: n m
    # Line 1: a11 a12 a13 ... a1m
    # Line 2: a21 a22 a23 ... a2m
    # ...
    # Line n: an1 an2 an3 ... anm
    # Line n+1: b1 b2 b2 ... bn
    # Line n+2: c1 c2 c3 ... cm
    #
    # Matrix equation: Ax <= b
    # Objective function: cx
    # n = number of inequalities
    # m = number of variables
    # a = coefficients of matrix A
    # b = coefficients of vector b
    # c = coefficients of vector c
    n, m = list(map(int, input().split()))
    tableau = np.zeros((n+1,m+1), dtype=np.float64)
    for i in range(n):
        for j, j2 in enumerate(map(float, input().split())):
            tableau[i+1][j+1] = -j2
    for i, i2 in enumerate(map(float, input().split())):
        tableau[i+1][0] = i2
    for i, i2 in enumerate(map(float, input().split())):
        tableau[0][i+1] = i2
    '''
    # This is a test example where the number of pivoting operation
    # increases exponentially with the size n
    n = 22
    m = n
    tableau = np.zeros((n+1,n+1), dtype=np.float64)
    for i in range(n):
        tableau[i+1][i+1] = -1
    for i in range(n):
        tableau[i+1][1:i+1] = -2
    for i in range(n):
        tableau[i+1][0] = 2**(i)
    tableau[0] = 1
    '''
    sim = Simplex(n, m)
    solution = sim.solve(tableau)
    if solution == "Infinity":
        print("Infinity")
    elif solution == "No solution":
        print("No solution")
    else:
        print("Bounded solution")
        print(" ".join(list(map(lambda x : '%.18f' % x, solution))))
