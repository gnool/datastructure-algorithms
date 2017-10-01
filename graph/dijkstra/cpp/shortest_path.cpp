#include <iostream>
#include <limits>
#include "shortest_path.h"

using namespace std;

// Constructor that initializes the member variables.
ShortestPath::ShortestPath(Graph graph, unsigned int source) {
  this->graph = graph;
  this->size_ = graph.vertices();
  (this->distance_).resize(graph.vertices());
  (this->previous).resize(graph.vertices(),-1);  // -1 represents unreachable
  this->source_ = source;
}

// Use Dijkstra's algorithm to find distance between source and all other vertices.
void ShortestPath::findDistanceToAll() {
  if (source_ > size_-1) {
    cerr << "Error: Source not in graph." << endl;
    return;
  }
  PriorityQueue<int> queue; // implement a priority queue for Dijkstra's algorithm
  previous.resize(size_,-1);  // -1 represents unreachable
  //  Initialize distances from source to all vertices to infinity.
  for (unsigned int i = 0; i < size_; i++) {
    // Distance from source to source is zero.
    if (i == source_) {
      distance_[i] = 0;
    }
    else {
      distance_[i] = numeric_limits<double>::infinity();
    }
    // Add vertice to priority queue.
    queue.push(make_tuple(i,distance_[i]));
  }
  tuple<int,double> current;  // Store the current min vertice popped from priority queue
  vector<tuple<int,double>> neighbours_list;  // Adjacent vertices
  while (!queue.isEmpty()) {
    current = queue.pop();
    neighbours_list = graph.neighbours(get<0>(current));  // get list of neighbours
    tuple<int,double> neighbour;
    for (unsigned int i = 0; i < neighbours_list.size(); i++) {
      neighbour = neighbours_list[i];
      // get<0>(neighbour) is neighbour's index number
      // get<1>(neighbour) is edge weight between current and neighbour
      if (distance_[get<0>(neighbour)] > get<1>(current) + get<1>(neighbour)) {
        distance_[get<0>(neighbour)] = get<1>(current) + get<1>(neighbour);
        previous[get<0>(neighbour)] = get<0>(current);
        queue.updateKey(get<0>(neighbour),distance_[get<0>(neighbour)]);
      }
    }
  }
}

// Calculate average path length from source to other vertices.
double ShortestPath::averagePathLength() {
  unsigned int count = 0;  // keep track of number of reachable vertices
  double total_distance = 0;  // sum of distances to reachable vertices
  for (unsigned int v = 1; v < size_; v++) {
    // If the target vertice is unreachable, skip it.
    if (distance_[v] == numeric_limits<double>::infinity()) {
      continue;
    }
    count++;
    total_distance += distance_[v];
  }
  // Calculate and return average path length.
  if (count == 0) {
    return numeric_limits<double>::infinity();
  }
  return total_distance/count;
}

// Return distance from source to target.
double ShortestPath::distance(unsigned int target) {
  if (target > size_-1) {
    cerr << "Error: Target not in graph." << endl;
    return 1;
  }
  return distance_[target];
}

// Print a sequence of vertices representing path from source to target.
void ShortestPath::printPath(unsigned int target) {
  if (target > size_-1) {
    cerr << "Error: Target not in graph." << endl;
    return;
  }
  vector<unsigned int> vertices;  // hold the list of vertices from source to target
  vertices.push_back(target);
  while (previous[target] != -1) {
    vertices.push_back(previous[target]);
    target = previous[target];
  }
  // There might be no path to source.
  if (vertices[vertices.size()-1] != source_) {
    cout << "There is no path from source to target." << endl;
  }
  // Else, print out the path.
  else {
    cout << "Printing path from source to target... (Format: Vertice(Distance from source))" << endl;
    for (int i = vertices.size()-1; i >= 0; i--) {
      cout << vertices[i] << "(" << distance_[vertices[i]] << ") ";
    }
    cout << endl;
  }
}

// Change to a new source.
void ShortestPath::source(unsigned int new_source) {
  source_ = new_source;
}

// Return current source.
unsigned int ShortestPath::source() {
  return source_;
}

// Return number of vertices in graph.
unsigned int ShortestPath::size() {
  return size_;
}