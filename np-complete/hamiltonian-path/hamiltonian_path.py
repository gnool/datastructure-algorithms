# python3

import itertools

class HamiltonianPath:
    """Hamiltonian path to SAT converter:

    Attributes:
        total_vertices    number of vertices
        total_edges       number of edges
        edges             list of edges

    Further details:
    Each state (i, j) represents whether vertex i is occupying position j in the
    Hamiltonian path (1 = yes, 0 = no)
    """
    def __init__(self):
        self.total_vertices = 0
        self.total_edges = 0
        self.edges = []

    def read_data(self):
        """Read input:

        Format:
        Line 0: n m
        Line 1: x1 y1
        Line 2: x2 y2
        ...
        Line m: xm ym

        n = number of vertices
        m = number of edges
        x, y = indices of vertices
        1 <= x,y <= n
        """
        self.total_vertices, self.total_edges = map(int, input().split())
        self.edges = [list(map(int, input().split())) for i in range(self.total_edges)]

    def var(self, i, j):
        """Return an integer representing a variable:

        Parameters:
        i             vertex index   [1, 2, 3, ...]
        j             color          [0, 1, 2, ...]
        """
        return (i-1) * self.total_vertices + j

    def vert_occupy_exactly_one_pos(self, i, clauses):
        """Impose restriction that each vertex occupy exactly one position
           in the Hamiltonian path.
           (a OR b OR c) AND (-a OR -b) AND (-a OR -c) AND (-b OR -c)
        """
        # (a OR b OR c OR ...)
        clause = [self.var(i, j) for j in range(1, self.total_vertices+1)]
        clauses.append(clause)
        # (-a OR -b) AND (-a OR -c) AND ...
        for pair in itertools.combinations(clause,2):
           clauses.append([-l for l in pair])

    def pos_occupy_by_exactly_one_vert(self, j, clauses):
        """Impose restriction that each vertex occupy exactly one position
           in the Hamiltonian path.
           (a OR b OR c) AND (-a OR -b) AND (-a OR -c) AND (-b OR -c)
        """
        # (a OR b OR c OR ...)
        clause = [self.var(i, j) for i in range(1, self.total_vertices+1)]
        clauses.append(clause)
        # (-a OR -b) AND (-a OR -c) AND ...
        for pair in itertools.combinations(clause,2):
           clauses.append([-l for l in pair])

    def print_SAT(self):
        """Output the Hamiltonian Path problem in SAT form."""
        n = self.total_vertices
        edges = self.edges
        clauses = []
        adj = [[] for _ in range(n+1)] # Discard index 0
        # Each vertex must occupy exactly one position in the Hamiltonian path.
        for i in range(1, n+1):
            self.vert_occupy_exactly_one_pos(i, clauses)
        # Each position in path must be occupied by exactly one vertex.
        for j in range(1, n+1):
            self.pos_occupy_by_exactly_one_vert(j, clauses)
        # Convert edges to adjacency list.
        for edge in edges:
            adj[edge[0]].append(edge[1])
            adj[edge[1]].append(edge[0])
        # Each pair of consecutive position in the path must correspond to an edge.
        for i in range(1, n+1):
            # Find the set of vertices which are not connected to i directly (i.e. no edge).
            non_neighbours = set([i for i in range(1,n+1)]) - set(adj[i])
            non_neighbours.remove(i)
            for j in range(1, n):
                for k in non_neighbours:
                    # If position j is occupied by i, the next position j+1 must be occupied by a
                    # neighbour of i (i.e. not k).
                    clauses.append([-self.var(i, j),-self.var(k, j+1)])
        # Print number of clauses and number of variables
        print(len(clauses), n**2)
        # Print all clauses
        for clause in clauses:
            clause.append(0)
            print(" ".join(map(str,clause)))     


if __name__ == '__main__':
    path = HamiltonianPath()
    path.read_data()
    path.print_SAT()
