# Overview
Here are some implementations of the Dijkstra's algorithm (uni- or bi-directional) to find the shortest path between two nodes in a directed graph.

# Dijkstra's algorithm
`dijkstra.py` is a simple implementation of the Dijkstra's algorithm using `heapq.py`.

# Bi-directional Dijkstra's algorithm
`bi-dijsktra.py` implements the bi-directional Dijkstra's algorithm. A few notes about the implementation:
- The distances from source to nodes are stored in a dictionary rather than a list. As the number of nodes gets very large (say number of nodes > 10^6), the cost of initializing a long list is greater than the cost of slightly slower member access of dict (than list).
- `heapq.py` is used for access to faster C-implementation. While there is no key (priority) update function in `heapq.py`, it is fine to just push duplicate nodes into the heap (and ignore them during popping). It is possible to write your own priority queue with key update, but if it is pure Python then I suspect it will not be faster than using heapq.py even if you manage to keep the heap smaller (by updating rather than pushing). If you insist to write your own priority queue with key update, you should at least take a look at the source code of `heapq.py` to get some ideas of faster siftup/siftdown (by minimizing comparisons).
