#include <iostream>
#include "graph.h"

using namespace std;

// Default constructor.
Graph::Graph() {
  vertices_ = 0;
  edges_ = 0;
}

// Parameterized constructor.
Graph::Graph(int total_vertices) {
  vertices_ = total_vertices;
  edges_ = 0;
  adjacency.resize(total_vertices);
}

// Return number of vertices.
int Graph::vertices() {
  return vertices_;
}

// Return number of edges.
int Graph::edges() {
  return edges_;
}

// Add a new edge between source and target with weight.
void Graph::addEdge(int source, int target, double weight) {
  auto& list = adjacency[source];
  list.push_back(make_tuple(target,weight));
  edges_++;
}

// Delete an edge pointing from source to target.
void Graph::deleteEdge(int source, int target) {
  auto& list = adjacency[source];
  tuple<int,double> edge;
  for (unsigned int i = 0; i < list.size(); i++) {
    edge = list[i];
    if (get<0>(edge) != target) {
      continue;
    }
    list.erase(list.begin()+i,list.begin()+i+1);
    break;
  }
}

// Update the edge from source to target with new weight.
void Graph::updateEdge(int source, int target, double new_weight) {
  auto& list = adjacency[source];
  for (unsigned int i = 0; i < list.size(); i++) {
    {
      // Since reference is not rebindable, edge is redefined in every iteration.
      auto& edge = list[i];
      // Skip if it is not the correct edge.
      if (get<0>(edge) != target) {
        continue;
      }
      // Update edge with new weight and exit loop.
      get<1>(edge) = new_weight;
      break;
    }
  }
}

// Return 1 if there is an edge from source to target.
int Graph::hasEdge(int source, int target) {
  auto& list = adjacency[source];
  tuple<int,double> edge;
  for (unsigned int i = 0; i < list.size(); i++) {
    edge = list[i];
    if (get<0>(edge) == target) {
      return 1;
    }
  }
  return 0;
}

// Return the weight of edge from source to target.
double Graph::edge(int source, int target) {
  auto& list = adjacency[source];
  tuple<int,double> edge;
  for (unsigned int i = 0; i < list.size(); i++) {
    edge = list[i];
    if (get<0>(edge) == target) {
      return get<1>(edge);
    }
  }
  cerr << "Error: No edge from source to target." << endl;
  return 0;
}

// Return a vector of tuples, each tuple represents one neighbour.
vector<tuple<int,double>> Graph::neighbours(int vertex_index) {
  return adjacency[vertex_index];
}