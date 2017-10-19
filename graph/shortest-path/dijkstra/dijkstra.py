#Uses python3

import sys
import heapq

def distance(adj, cost, s, t):
    n = len(adj)
    dist = [-1]*n
    dist[s] = 0
    h = []
    heapq.heappush(h,(0,s))
    while h:
        min_v = heapq.heappop(h)[1]
        if min_v == t:
            return dist[t]
        for i, v in enumerate(adj[min_v]):
            if dist[v] == -1:
                dist[v] = dist[min_v] + cost[min_v][i]
                heapq.heappush(h,(dist[v],v))
            elif dist[v] > dist[min_v] + cost[min_v][i]:
                dist[v] = dist[min_v] + cost[min_v][i]
                heapq.heappush(h,(dist[v],v))
    return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
