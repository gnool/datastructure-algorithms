#ifndef SIMULATOR_H
#define SIMULATOR_H

#include <random>
#include "graph.h"

// Class which handles building of random graph (via Monte Carlo simulation) as well as 
// calling ShortestPath to generate shortest path distances from source = 0. It also
// calculates the average path length from source to all other vertices.
class Simulator {
  public:
    // Parameterized constructor that initializes the member variables.
    Simulator(unsigned int size, double density, double min_distance, double max_distance);
    // Estimate the average path length by averaging over specified number of iterations.
    // Default: 1 iteration
    double calcAveragePathLength(unsigned int iterations = 1);
    // Build a random graph with given size, density, minimum and maximum edge weight.
    Graph buildGraph();
    // Return number of vertices.
    unsigned int size();
    // Update number of vertices.
    void size(unsigned int new_size);
    // Return edge density.
    double density();
    // Update edge density.
    void density(double new_density);
    // Return minimum edge weight.
    double min_distance();
    // Update minimum edge weight.
    void min_distance(double new_min_distance);
    // Return maximum edge weight.
    double max_distance();
    // Update maximum edge weight.
    void max_distance(double new_max_distance);
    
  private:
    // Total number of vertices in graph.
    unsigned int size_;
    // Edge density.
    double density_;
    // Minimum edge weight.
    double min_distance_;
    // Maximum edge weight.
    double max_distance_;
    // Mersenne Twister RNG (for edge density).
    std::mt19937 mt_rand;
    // Mersenne Twister RNG (for edge weight).
    std::mt19937 mt_rand2;
};

#endif