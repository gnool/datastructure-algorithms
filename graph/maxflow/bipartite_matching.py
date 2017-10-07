# python3

import queue

class Edge:
    """Edge of graph

    Attributes:
        start           directed edge from start to end
        end             
        capacity        capacity
        flow            flow
    """
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0

class FlowGraph:
    """Max-flow graph

    Attributes:
        edges           List of Edge instances
                        Note: edges[u] and edges[v], where u is even, are a pair of
                        entries to represent an edge and its reverse edge. The reverse
                        edge only exists in the residual graph.
        graph           Adjacency list representation
        fast_find       Dictionary to find (u, v) in graph[u]
    """
    def __init__(self, n):
        self.edges = []
        self.graph = [[] for _ in range(n)]
        self.fast_find = {}
    def add_edge(self, from_, to, capacity):
        """Add a new edge to graph"""
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.fast_find[(from_,to)] = len(self.graph[from_])
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.fast_find[(to,from_)] = len(self.graph[to])
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)
    def size(self):
        """Number of nodes in graph"""
        return len(self.graph)
    def add_flow(self, id_, flow):
        """Update flow of edge"""
        # id_ and id_ ^ 1 form a pair of forward and reverse edge
        self.edges[id_].flow += flow
        self.edges[id_ ^ 1].flow -= flow
    def max_flow(self, from_, to):
        """Implementation of Edmonds-Karp algorithm"""
        flow = 0
        while True:
            previous = [None]*self.size()
            previous[from_] = from_
            # Use breadth-first search
            q = queue.Queue()
            q.put(from_)
            while not q.empty():
                # No need for further search if sink is reached
                if previous[to] != None:
                    break
                cur = q.get()
                ids = self.graph[cur]
                for i in ids:
                    edge = self.edges[i]
                    # Forward edge
                    if i % 2 == 0:
                        if previous[edge.end] == None and edge.capacity > edge.flow:
                            previous[edge.end] = cur
                            q.put(edge.end)
                    # Reverse edge (in residual graph)
                    else:
                        if previous[edge.end] == None and edge.flow != 0:
                            previous[edge.end] = cur
                            q.put(edge.end)
            # Update flow if there is an augmenting path in residual graph
            if previous[to] != None:
                # Find the minimum capacity along this path
                cur = to
                min_ = float('inf')
                while previous[cur] != cur:
                    id_ = self.graph[previous[cur]][self.fast_find[(previous[cur], cur)]]
                    edge = self.edges[id_]
                    # Forward edge
                    if id_ % 2 == 0:
                        min_ = min(min_, edge.capacity - edge.flow)
                    # Reverse edge (in residual graph)
                    else:
                        min_ = min(min_, -edge.flow)
                    cur = previous[cur]
                # Update all edges along this path
                cur = to
                while previous[cur] != cur:
                    id_ = self.graph[previous[cur]][self.fast_find[(previous[cur], cur)]]
                    self.add_flow(id_, min_)
                    cur = previous[cur]
                flow += min_
            # Otherwise, return the maximum flow
            else:
                return flow

class BipartiteMatching:
    """Bipartite matching using max-flow algorithm"""
    def read_data(self):
        """Read input
        Format:
        Line 0: n m
        Line 1: b11 b12 ... b1m
        Line 2: b21 b22 ... b2m
        Line n: bn1 bn2 ... bnm
        0 <= b <= 1 (b is boolean variable)
        """
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix
    def write_response(self, matching):
        """Output matching"""
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))
    def find_matching(self, adj_matrix):
        """Use class FlowGraph (Edmonds-Karp algorithm) to find max matching"""
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        matching = [-1] * n # -1 means no match
        graph = FlowGraph(n+m+2) # +2 for artificial source and sink
        for i in range(n):
            graph.add_edge(n+m, i, 1) # add edges from source
            for j in range(m):
                if adj_matrix[i][j] == 1:
                    graph.add_edge(i, n+j, 1) # add edges from input matrix
        for j in range(m):
            graph.add_edge(n+j, n+m+1, 1) # add edges to sink
        max_flow = graph.max_flow(n+m, n+m+1)
        # Find which nodes in left part has flow to nodes in right part
        for i in range(n):
            ids = graph.graph[i]
            for edge_id in ids:
                edge = graph.edges[edge_id]
                if edge.flow == 1:
                    matching[i] = edge.end-n
        return matching
    def solve(self):
        """ Read bipartite graph from input, find max matching and print output"""
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)

if __name__ == '__main__':
    bipartite_matching = BipartiteMatching()
    bipartite_matching.solve()
