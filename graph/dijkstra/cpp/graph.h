#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <tuple>

// Graph implemented using adjacency representation (i.e. edge lists).
// All vertices are numbered 0, 1, 2, ...
class Graph {
  public:
    // Default constructor.
    Graph();
    // Parameterized constructor.
    Graph(int total_vertices);
    // Return number of vertices.
    int vertices();
    // Return number of edges.
    int edges();
    // Add a new edge between source and target with weight.
    void addEdge(int source, int target, double weight);
    // Delete an edge pointing from source to target.
    void deleteEdge(int source, int target);
    // Update the edge from source to target with new weight.
    void updateEdge(int source, int target, double weight);
    // Return 1 if there is an edge from source to target.
    int hasEdge(int source, int target);
    // Return the weight of edge from source to target.
    double edge(int source, int target);
    // Return a vector of tuples, each tuple representing one neighbour.
    std::vector<std::tuple<int,double>> neighbours(int vertex_index);
    
  private:
    // Total vertices.
    int vertices_;
    // Total edges.
    int edges_;
    // Adjacency representation of graph.
    // Basically a 2D-vector storing tuples, where each tuple represents a neighbour
    // and contains the neighbour's vertex id as well as the edge weight between them.
    std::vector<std::vector<std::tuple<int,double>>> adjacency;
};

#endif