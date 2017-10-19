#Uses python3

import heapq
from math import sqrt

class Graph:
    """Graph represented in adjacency list.

    Attributes:
        edges        number of edges
        nodes        number of nodes
        adj          adjacency list
        adjR         adjacency list of reverse graph
        coor         coordinates (x, y)
    """
    def __init__(self, m, n):
        self.edges = m
        self.nodes = n
        self.adj = [[] for _ in range(n+1)]
        self.adjR = None
        self.coor = [None]*(n+1)

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
        """Compute shortest distance using bidirectional A* algorithm."""
        if start == end:
            return 0
        if self.adjR == None:
            self.build_reverse_graph()
        n = self.nodes
        m = self.edges
        adj = self.adj
        adjR = self.adjR
        sx = self.coor[start][0]
        sy = self.coor[start][1]
        tx = self.coor[end][0]
        ty = self.coor[end][1]
        adjustment = sqrt((tx-sx)**2 + (ty-sy)**2)  # add to final result
        # For forward search
        processed = set()
        potential = {}
        dist = {}
        dist[start] = 0
        heap = []
        potential[start] = adjustment/2
        heapq.heappush(heap,(0, start))
        # For backward search
        processedB = set()
        potentialB = {}
        distB = {}
        distB[end] = 0
        heapB = []
        potentialB[end] = adjustment/2
        heapq.heappush(heapB,(0, end))
        shortest = float('inf')
        while heap and heapB:
            # For forward search
            if heap:
                d, u = heapq.heappop(heap)
                if u not in processed:
                    processed.add(u)
                    dist1 = potential[u]
                    for v, w in adj[u]:
                        if v in processed:
                            continue
                        (x, y) = self.coor[v]
                        if v in potential:
                            dist2 = potential[v]
                        else:
                            dist2 = (sqrt((x-tx)**2 + (y-ty)**2) - sqrt((x-sx)**2 + (y-sy)**2))/2
                            potential[v] = dist2
                        new_dist = dist[u] + w - dist1 + dist2
                        if dist.get(v, -1) == -1:
                            dist[v] = new_dist
                            heapq.heappush(heap,(new_dist, v))
                        elif dist[v] > new_dist:
                            dist[v] = new_dist
                            heapq.heappush(heap,(new_dist, v))
                        if v in processedB:
                            length = distB[v] + new_dist
                            if length < shortest:
                                shortest = length
                    if u in processedB:
                        return shortest + adjustment
            else:
                return shortest + adjustment
            # For backward search
            if heapB:
                d, u = heapq.heappop(heapB)
                if u not in processedB:
                    processedB.add(u)
                    dist1 = potentialB[u]
                    for v, w in adjR[u]:
                        if v in processedB:
                            continue
                        (x, y) = self.coor[v]
                        if v in potentialB:
                            dist2 = potentialB[v]
                        else:
                            dist2 = potentialB.get(v, (sqrt((x-sx)**2 + (y-sy)**2) - sqrt((x-tx)**2 + (y-ty)**2))/2)
                            potentialB[v] = dist2
                        new_dist = distB[u] + w - dist1 + dist2
                        if distB.get(v, -1) == -1:
                            distB[v] = new_dist
                            heapq.heappush(heapB,(new_dist, v))
                        elif distB[v] > new_dist:
                            distB[v] = new_dist
                            heapq.heappush(heapB,(new_dist, v))
                        if v in processed:
                            length = dist[v] + new_dist
                            if length < shortest:
                                shortest = length
                    if u in processed:
                        return shortest + adjustment
            else:
                return shortest + adjustment
        return -1


if __name__ == '__main__':
    # Input format
    # Line 0:       n m
    # Line 1:       x1 y1
    # Line 2:       x2 y2
    # ...
    # Line n:       xn yn
    # Line n+1:     u1 v1 w1
    # Line n+2:     u2 v2 w2
    # ...
    # Line n+m:     um vm wm
    # Line n+m+1:   q
    # Line n+m+2:   s1 t1
    # Line n+m+3:   s2 t2
    # ...
    # Line n+m+q+1: sq tq
    # x,y  :  Cartesian coordinates
    # 1 <= s,t,u,v <= n  :  nodes in 1-based indices
    # q  :  number of queries for path distance between node s and node t
    # n  :  number of nodes
    # m  :  number of edges
    n, m = list(map(int, input().split()))
    graph = Graph(m, n)
    for i in range(1, n+1):
        (x, y) = list(map(int, input().split()))
        graph.coor[i] = (x, y)
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
        else:
            dist = int(round(dist))
        results.append(dist)
    print(" ".join(list(map(str, results))))
    
