#include <iostream>
#include <limits>
#include "simulator.h"
#include "shortest_path.h"

using namespace std;

// Parameterized constructor that initializes the member variables.
Simulator::Simulator(unsigned int size, double density, double min_distance, double max_distance) {
  this->size_ = size;
  this->density_ = density;
  this->min_distance_ = min_distance;
  this->max_distance_ = max_distance;
  mt_rand.seed(rand());  // seed Mersenne Twister RNG (for edge probability)
  mt_rand2.seed(rand());  // seed Mersenne Twister RNG (for edge weight)
}

// Build a random graph with given size, density, minimum and maximum edge weight.
Graph Simulator::buildGraph() {
  double weight;
  // Uniform distribution [0,1] for probability of creating an edge.
  uniform_real_distribution<> dis(0,1);
  // Uniform distribution [min,max] for the edge weight.
  uniform_real_distribution<> dis2(min_distance_,max_distance_);
  // Initialize a graph with given size.
  Graph graph(size_);
  for (unsigned int i = 0; i < size_; i++) {
    for (unsigned int j = i+1; j < size_; j++) {
      // Recall that mt_rand is for edge probability, while mt_rand2 is for
      // edge weight.
      if (dis(mt_rand) < density_) {
        weight = dis2(mt_rand2);  // generate random edge weights
        graph.addEdge(i,j,weight);
        graph.addEdge(j,i,weight);
      }
    }
  }
  return graph;
}

// Estimate the average path length by averaging over specified number of iterations.
double Simulator::calcAveragePathLength(unsigned int iterations) {
  double iteration_sum = 0, average_path_length;
  for (unsigned int i = 0; i < iterations; i++) {
    ShortestPath path(buildGraph(),0);  // set source to 0
    path.findDistanceToAll();  // find shortest distance to all vertices from source
    average_path_length = path.averagePathLength();
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