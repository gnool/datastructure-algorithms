# python3

class CNF2:
    """Class for solving 2-CNF problem.

    Attributes:
        var        number of variables
    """
    def __init__(self):
        self.var = 0
    
    def read_data(self):
        """Read input:

        Format:
        Line 0: n m
        Line 1: v11 v12
        Line 2: v21 v22
        ...
        Line m: vm1 vm2
        -n <= v <= n; v != 0
        """
        n, m = map(int, input().split())
        clauses = [ list(map(int, input().split())) for i in range(m) ]
        self.var = n
        return (clauses, n, m)

    def solve(self):
        """Solve the 2-CNF problem."""
        (clauses, n, m) = self.read_data()
        # In adj[0:n] is for the n variables, while adj[n:2n] is for
        # their negations (e.g. adj[0] and adj[n] form a pair).
        adj = [[] for _ in range(2*n)]
        for x, y in clauses:
            adj[self.index(-y)].append(self.index(x))
            adj[self.index(-x)].append(self.index(y))
        # Find strongly connected components
        scc = SCC(adj)
        components = scc.components
        results = [None]*2*n
        for c in components:
            # If a variable and its complement exists concurrently
            # in the same component, the clauses are unsatisfiable.
            set_ = set(c)
            for i in set_:
                if self.complement(i) in set_:
                    return 'UNSATISFIABLE'
            # Otherwise, assign 1 to all nodes in current component,
            # and assign 0 to all their negations.
            if results[c[0]] == None:
                for i in c:
                    results[i] = 1
                    if i < n:
                        results[i+n] = 0
                    else:
                        results[i-n] = 0
        results = [-(i+1) if results[i] == 0 else i+1 for i in range(len(results))]
        return results[0:n]

    def index(self, i):
        """Return array index used internally."""
        if i < 0:
            return self.var + abs(i) - 1
        else:
            return i - 1

    def complement(self, i):
        """Return original variable index."""
        if i < self.var:
            return i + self.var
        else:
            return i - self.var


class SCC:
    """Strongly connected component (SCC) finder

    Attributes:
        components    a list of components (expressed in list)
    """
    def __init__(self, adj):
        self.components = self.solve(adj)

    def solve(self, adj):
        """Find strongly connected components."""
        n = len(adj)
        # Build reversed graph
        adjR = [[] for _ in range(n)]
        for i in range(n):
            for j in adj[i]:
                adjR[j].append(i)
        # DFS-explore reversed graph adjR
        post = self.post_order(adjR)
        # Sort and start processing the largest postorder vertices
        post.sort(reverse=True)
        visited = [0]*n
        components = []
        for _, i in post:
            if visited[i] != 1:
                explored = self.dfs(adj, visited, i)
                components.append(explored)
        return components

    def dfs(self, adj, visited, x):
        """Depth-first-search graph."""
        explored = [x]
        n = len(adj)
        stack = []
        cur = x
        stack.append((0, x))
        while stack:
            ip, cur = stack.pop()
            visited[cur] = 1
            pop_stack = False
            for i in range(ip, len(adj[cur])):
                if visited[adj[cur][i]] != 1:
                    explored.append(adj[cur][i])
                    stack.append((i+1, cur))
                    stack.append((0, adj[cur][i]))
                    pop_stack = True
                    break
            if pop_stack:
                continue
        return explored

    def post_order(self, adj):
        """Find post-order using depth-first-search."""
        count = 1
        n = len(adj)
        post = [None]*n
        visited = [0]*n
        for j in range(n):
            if visited[j] == 1:
                continue
            stack = []
            cur = j
            stack.append((0, j))
            while stack:
                ip, cur = stack.pop()
                visited[cur] = 1
                pop_stack = False
                for i in range(ip, len(adj[cur])):
                    if visited[adj[cur][i]] != 1:
                        stack.append((i+1, cur))
                        stack.append((0, adj[cur][i]))
                        pop_stack = True
                        break
                if pop_stack:
                    continue
                post[cur] = (count, cur)
                count += 1
        return post


if __name__ == '__main__':
    cnf = CNF2()
    results = cnf.solve()
    if results == 'UNSATISFIABLE':
        print('UNSATISFIABLE')
    else:
        print('SATISFIABLE')
        print(" ".join(list(map(str,results))))
