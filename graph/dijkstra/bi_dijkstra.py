#Uses python3

import heapq

class Graph:
    """Graph represented in adjacency list.

    Attributes:
        edges        number of edges
        nodes        number of nodes
        adj          adjacency list
        adjR         adjacency list of reverse graph
    """
    def __init__(self, m, n):
        self.edges = m
        self.nodes = n
        self.adj = [[] for _ in range(n+1)]
        self.adjR = None

    def add_edge(self, u, v, w):
        """Add a new edge."""
        self.adj[u].append((v, w))

    def build_reverse_graph(self):
        """Build the reverse graph."""
        adj = self.adj
        self.adjR = [[] for _ in range(n+1)]
        adjR = self.adjR
        for u, edges in enumerate(adj):
            for v, w in edges:
                adjR[v].append((u, w))
        
    def distance(self, start, end):
        """Compute shortest distance using bidirectional Dijkstra's algorithm."""
        if start == end:
            return 0
        if self.adjR == None:
            self.build_reverse_graph()
        n = self.nodes
        m = self.edges
        adj = self.adj
        adjR = self.adjR
        # For forward search
        processed = set()
        dist = {}
        dist[start] = 0
        heap = []
        heapq.heappush(heap,(0, start))
        # For backward search
        processedB = set()
        distB = {}
        distB[end] = 0
        heapB = []
        heapq.heappush(heapB,(0, end))
        shortest = float('inf')
        while heap and heapB:
            # For forward search
            if heap:
                d, u = heapq.heappop(heap)
                if u not in processed:
                    processed.add(u)
                    for v, w in adj[u]:
                        if dist.get(v, -1) == -1:
                            dist[v] = dist[u] + w
                            heapq.heappush(heap,(dist[v], v))
                        elif dist[v] > dist[u] + w:
                            dist[v] = dist[u] + w
                            heapq.heappush(heap,(dist[v], v))
                    if dist[u] < shortest:
                        for v, w in adj[u]:
                            if v in processedB:
                                length = dist[u] + distB[v] + w
                                if length < shortest:
                                    shortest = length
                    if u in processedB:
                        return shortest
            else:
                return shortest
            # For backward search
            if heapB:
                d, u = heapq.heappop(heapB)
                if u not in processedB:
                    processedB.add(u)
                    for v, w in adjR[u]:
                        if distB.get(v, -1) == -1:
                            distB[v] = distB[u] + w
                            heapq.heappush(heapB,(distB[v], v))
                        elif distB[v] > distB[u] + w:
                            distB[v] = distB[u] + w
                            heapq.heappush(heapB,(distB[v], v))
                    if distB[u] < shortest:
                        for v, w in adjR[u]:
                            if v in processed:
                                length = distB[u] + dist[v] + w
                                if length < shortest:
                                    shortest = length
                    if u in processed:
                        return shortest
            else:
                return shortest
        return -1


if __name__ == '__main__':
    # Input format
    # Line 0:     n m
    # Line 1:     u1 v1 w1
    # Line 2:     u2 v2 w2
    # ...
    # Line m:     um vm wm
    # Line m+1:   q
    # Line m+2:   s1 t1
    # Line m+3:   s2 t2
    # ...
    # Line m+q+1: sq tq
    # 0 <= s,t,u,v <= n   (nodes in either 0- or 1-based indices)
    # q: number of queries for path distance between node s and node t
    # n: number of nodes
    # m: number of edges
    n, m = list(map(int, input().split()))
    graph = Graph(m, n)
    for i in range(m):
        (u, v, w) = list(map(int, input().split()))
        graph.add_edge(u, v, w)
    q = int(input())
    queries = []
    for i in range(q):
        (u, v) = list(map(int, input().split()))
        queries.append((u, v))
    results = []
    for u, v in queries:
        dist = graph.distance(u, v)
        if dist == float('inf'):
            dist = -1
        results.append(dist)
    print(" ".join(list(map(str, results))))
