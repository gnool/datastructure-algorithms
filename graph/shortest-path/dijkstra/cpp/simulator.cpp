#include <iostream>
#include <limits>
#include "simulator.h"

using namespace std;

// Default constructor.
Simulator::Simulator() {
  mt_rand.seed(rand());  // seed Mersenne Twister RNG (for edge probability)
  mt_rand2.seed(rand());  // seed Mersenne Twister RNG (for edge weight)
}

// Parameterized constructor that involves building the graph directly.
Simulator::Simulator(unsigned int size, double density, double min_distance, double max_distance) {
  // Store the graph configuration in member variables.
  size_ = size;
  density_ = density;
  min_distance_ = min_distance;
  max_distance_ = max_distance;
  mt_rand.seed(rand());  // seed Mersenne Twister RNG (for edge probability)
  mt_rand2.seed(rand());  // seed Mersenne Twister RNG (for edge weight)
  // Build the graph.
  buildGraph(size, density, min_distance, max_distance);
  findShortestPath();
}

// Build a random graph with given size, density, minimum and maximum edge weight.
void Simulator::buildGraph(unsigned int size, double density, double min_distance, double max_distance) {
  // Store the graph configuration in member variables.
  size_ = size;
  density_ = density;
  min_distance_ = min_distance;
  max_distance_ = max_distance;
  // Uniform distribution [0,1] for probability of creating an edge.
  uniform_real_distribution<> dis(0,1);
  // Uniform distribution [min,max] for the edge weight.
  uniform_real_distribution<> dis2(min_distance,max_distance);
  // Initialize a graph with given size.
  Graph new_graph(size);
  for (unsigned int i = 0; i < size; i++) {
    for (unsigned int j = i+1; j < size; j++) {
      // Recall that mt_rand is for edge probability, while mt_rand2 is for
      // edge weight.
      if (dis(mt_rand) < density) {
        double weight = dis2(mt_rand2);  // generate random edge weights
        new_graph.addEdge(i,j,weight);
        new_graph.addEdge(j,i,weight);
      }
    }
  }
  graph_ = new_graph;
}

// Find the shortest paths from source to all other vertices based on the member graph_.
void Simulator::findShortestPath() {
  ShortestPath new_path(graph_,0);  // set source to 0
  new_path.findDistanceToAll();  // find shortest paths from source to all other vertices
  path_ = new_path;
}

// Estimate the average path length by averaging over specified number of iterations.
double Simulator::calcAveragePathLength(unsigned int iterations) {
  // If iterations is set to zero, the simulator returns average path length of the existing member graph.
  if (!iterations) {
    return path_.averagePathLength();
  }
  // Otherwise, create different random graphs and average the average path length over the iterations.
  double iteration_sum = 0, average_path_length;
  for (unsigned int i = 0; i < iterations; i++) {
    buildGraph(size_, density_, min_distance_, max_distance_);
    findShortestPath();
    average_path_length = path_.averagePathLength();
    if (average_path_length == numeric_limits<double>::infinity()) continue;
    iteration_sum += average_path_length;
  }
  return iteration_sum/iterations;
}

// Return number of vertices.
unsigned int Simulator::size() {
  return size_;
}

// Update number of vertices.
void Simulator::size(unsigned int new_size) {
  size_ = new_size;
}

// Return edge density.
double Simulator::density() {
  return density_;
}

// Update edge density.
void Simulator::density(double new_density) {
  density_ = new_density;
}

// Return minimum edge weight.
double Simulator::min_distance() {
  return min_distance_;
}

// Update minimum edge weight.
void Simulator::min_distance(double new_min_distance) {
  min_distance_ = new_min_distance;
}

// Return maximum edge weight.
double Simulator::max_distance() {
  return max_distance_;
}

// Update maximum edge weight.
void Simulator::max_distance(double new_max_distance) {
  max_distance_ = new_max_distance;
}

// Return the Graph instance currently stored.
Graph Simulator::graph() const {
  return graph_;
}

// Return the ShortestPath instance currently stored.
ShortestPath Simulator::path() const {
  return path_;
}
