# python3

import queue
import math

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
            previous[0] = 0
            # Use breadth-first search
            q = queue.Queue()
            q.put(0)
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
                min_ = math.inf
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

def read_data():
    """Get user input
    Format:
    Line 0: n m
    Line 1: s1 t1 c1
    Line 2: s2 t2 c2
    ...
    Line m: sm tm cm

    n:     Number of nodes
    m:     Number of edges
    s, t:  Edge from node index s to node index t
    c:     Edge capacity
    1 <= s,t <= n  (1-based indices)

    Note: source and sink indices must be 1 and n respectively
    """
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    edge_dict = {}
    # Preprocess the input (sum capacities from all u->v edges)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        if u == v:
            continue
        if v == 1:
            continue
        if (u, v) in edge_dict:
            edge_dict[(u, v)] += capacity
        else:
            edge_dict[(u, v)] = capacity
    # Add all edges to graph
    for (u, v), capacity in edge_dict.items():
        graph.add_edge(u - 1, v - 1, capacity)
    return graph

if __name__ == '__main__':
    graph = read_data()
    print(graph.max_flow(0, graph.size() - 1))
