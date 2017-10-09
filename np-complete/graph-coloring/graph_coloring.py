# python3

import itertools

class GraphColoring:
    """Graph coloring to SAT converter:

    Attributes:
        edges:           list of edges
        total_vertices:  number of vertices
        total_edges:     number of edges
        colors:          number of colors

    Further details:
    Each state (i, j) represents whether vertice i is colored by color j
    (1 = yes, 0 = no)
    """
    def __init__(self, colors):
        self.edges = []
        self.total_vertices = 0
        self.total_edges = 0
        self.colors = colors

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
        i             vertice index  [1, 2, 3, ...]
        j             color          [0, 1, 2, ...]
        """
        return (i-1) * self.colors + j

    def exactly_one(self, i, clauses):
        """Impose restriction that each vertex must be assigned to
           exactly one color.
           (a OR b OR c) AND (-a OR -b) AND (-a OR -c) AND (-b OR -c)
        """
        # (a OR b OR c OR ...)
        clause = [self.var(i, j) for j in range(1, self.colors+1)]
        clauses.append(clause)
        # (-a OR -b) AND (-a OR -c) AND ...
        for pair in itertools.combinations(clause, 2):
           clauses.append([-l for l in pair])

    def print_SAT(self):
        """Output the graph coloring problem in SAT form."""
        clauses = []
        n = self.total_vertices
        # Each vertex must be assigned to exactly one color.
        for i in range(1, n+1):
            self.exactly_one(i, clauses)
        # Neighbours must be differently colored (P NAND Q)
        for edge in self.edges:
            for j in range(1, self.colors+1):
                clauses.append([-self.var(edge[0],j), -self.var(edge[1],j)])
        # Print number of clauses and number of variables
        print(len(clauses), n*self.colors)
        # Print all clauses
        for clause in clauses:
            clause.append(0)
            print(" ".join(map(str, clause)))


if __name__ == '__main__':
    graph = GraphColoring(3)
    graph.read_data()
    graph.print_SAT()
