#ifndef SHORTEST_PATH_H
#define SHORTEST_PATH_H

#include <vector>
#include <tuple>
#include "graph.h"
#include "priority_queue.h"

// Implementation of Dijkstra's algorithm that calculates shortest distances from
// source to all other vertices. Any instance of this class can be reused by first
// using source(new source) to renew the source, then call findDistanceToAll() again
// to recalculate the shortest distance to all other vertices from the new source.
class ShortestPath {
  public:
    // Default constructor.
    ShortestPath();
    // Parameterized constructor that initializes the member variables.
    ShortestPath(Graph graph, unsigned int source);
    // Use Dijkstra's algorithm to find distance between source and all other vertices.
    void findDistanceToAll();
    // Calculate average path length from source to other vertices.
    double averagePathLength() const;
    // Return distance from source to target.
    double distance(unsigned int target);
    // Print a sequence of vertices representing path from source to target.
    void printPath(std::ostream& os, unsigned int target) const;
    // Change to a new source.
    void source(unsigned int new_source);
    // Return current source.
    unsigned int source() const;
    // Return number of vertices in graph.
    unsigned int size() const;
    
  private:
    // Graph class to store the graph.
    Graph graph;
    // Number of vertices.
    unsigned int size_;
    // Vertice marked as source.
    unsigned int source_;
    // Distance from source to all other vertices.
    std::vector<double> distance_;
    // Used to reconstruct the shortest path.
    std::vector<int> previous;
};

std::ostream& operator<<(std::ostream& os, const ShortestPath& path);

#endif
