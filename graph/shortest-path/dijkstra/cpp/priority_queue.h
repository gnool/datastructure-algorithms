#ifndef PRIORITY_QUEUE_H
#define PRIORITY_QUEUE_H

#include <iostream>
#include <vector>
#include <tuple>
#include <unordered_map>

// Class PriorityQueue implements the priority queue using the binary min heap.
// Each node in the heap consists of a tuple (data,key), where key is used as
// the comparison between any two nodes. Furthemore it utilizes an unordered
// map for O(1) search operation.
template <typename ValueType>
class PriorityQueue {
  public:
    // Push a new node to the priority queue.
    void push(std::tuple<ValueType,double> new_node);
    // Pop the node from the top of the priority queue.
    std::tuple<ValueType,double> pop();
    // Return the node at the top of the priority queue (without popping).
    std::tuple<ValueType,double> peek();
    // Return 1 if priority queue is empty, 0 otherwise.
    int isEmpty();
    // Return number of nodes in priority queue.
    unsigned int size();
    // Return 1 if input data is in priority queue, 0 otherwise.
    int inQueue(ValueType data);
    // Return the priority of input data. Priority = 0 means minimum.
    unsigned int getPriority(ValueType data);
    // Update the key of specified input data.
    void updateKey(ValueType data, double new_key);
    // Perform sift down operation on input node to restore heap property.
    void siftDown(unsigned int node_index);
    // Perform sift up operation on input node to restore heap property.
    void siftUp(unsigned int node_index);
    
  private:
    // For O(1) search of data.
    std::unordered_map<ValueType,int> index_map;
    // Each tuple represents (data,key).
    std::vector<std::tuple<ValueType,double>> nodes;
    // Return parent's node index.
    unsigned int parent(unsigned int node_index);
    // Return left child's node index.
    unsigned int leftChild(unsigned int node_index);
    // Return right child's node index.
    unsigned int rightChild(unsigned int node_index);
};

// Implementation section

// Push a new node to the priority queue.
template <typename ValueType>
void PriorityQueue<ValueType>::push(std::tuple<ValueType,double> new_node) {
  // Add new node to the last position of heap to preserve heap shape.
  nodes.push_back(new_node);
  // Add the new entry to hash table for faster lookup later.
  index_map[std::get<0>(new_node)] = nodes.size()-1;
  // Restore heap structure.
  siftUp(nodes.size()-1);
}

// Pop the node from the top of the priority queue.
template <typename ValueType>
std::tuple<ValueType,double> PriorityQueue<ValueType>::pop() {
  std::tuple<ValueType,double> min = nodes[0];
  // Move the last node to the root to preserve heap shape.
  nodes[0] = nodes[nodes.size()-1];
  nodes.pop_back();
  // Remove data from hash table.
  index_map.erase(std::get<0>(min));
  // Restore heap structure.
  siftDown(0);
  return min;
}

// Return the node at the top of the priority queue (without popping).
template <typename ValueType>
std::tuple<ValueType,double> PriorityQueue<ValueType>::peek() {
  return nodes[0];
}

// Return 1 if priority queue is empty, 0 otherwise.
template <typename ValueType>
int PriorityQueue<ValueType>::isEmpty() {
  if (nodes.size() == 0) {
    return 1;
  }
  else {
    return 0;
  }
}

// Return number of nodes in priority queue.
template <typename ValueType>
unsigned int PriorityQueue<ValueType>::size() {
  return nodes.size();
}

// Return 1 if input data is in priority queue, 0 otherwise.
template <typename ValueType>
int PriorityQueue<ValueType>::inQueue(ValueType data) {
  if (index_map.find(data) != index_map.end()) {
    return 1;
  }
  else {
    return 0;
  }
}

// Return the priority of input data. Priority = 0 means minimum.
template <typename ValueType>
unsigned int PriorityQueue<ValueType>::getPriority(ValueType data) {
  if (!inQueue(data)) {
    std::cerr << "Error: Data not in queue." << std::endl;
    return 0;
  }
  return index_map[data];
}

// Update the key of specified input data.
template <typename ValueType>
void PriorityQueue<ValueType>::updateKey(ValueType data, double new_key) {
  // Instead of update, insert as new node if it is not in queue.
  if (!inQueue(data)) {
    push(std::make_tuple(data,new_key));
    return;
  }
  // Otherwise update existing node in the heap.
  int index = getPriority(data);
  double old_key = std::get<1>(nodes[index]);
  std::get<1>(nodes[index]) = new_key;
  // Restore heap structure.
  if (new_key > old_key) {
    siftDown(index);
  }
  else {
    siftUp(index);
  }
}

// Perform sift down operation on input node to restore heap property.
template <typename ValueType>
void PriorityQueue<ValueType>::siftDown(unsigned int node_index) {
  int target, root = node_index;
  std::tuple<ValueType,double> swap;  // temporary variable for swapping
  // This loop only continues when the current root has a child.
  while (leftChild(root) < nodes.size()) {
    target = root;  // store the swap target
    // First compare with left child.
    if (std::get<1>(nodes[target]) > std::get<1>(nodes[leftChild(root)])) {
      target = leftChild(root);
    }
    // Then compare with right child (if it exists).
    if ((rightChild(root) < nodes.size()) && (std::get<1>(nodes[target]) > std::get<1>(nodes[rightChild(root)]))) {
      target = rightChild(root);
    }
    // Exit function if heap structure is fully restored.
    if (target == root) return;
    // Otherwise perform swapping with target child and update the new root.
    else {
      swap = nodes[root];
      nodes[root] = nodes[target];
      index_map[std::get<0>(nodes[target])] = root;
      nodes[target] = swap;
      index_map[std::get<0>(swap)] = target;
      root = target;
    }
  }
}

// Perform sift up operation on input node to restore heap property.
template <typename ValueType>
void PriorityQueue<ValueType>::siftUp(unsigned int node_index) {
  std::tuple<ValueType,double> swap;  // temporary variable for swapping
  // This loop continues as long as the parent's key is larger than current node's key.
  while (node_index > 0 && std::get<1>(nodes[parent(node_index)]) > std::get<1>(nodes[node_index])) {
    swap = nodes[node_index];
    nodes[node_index] = nodes[parent(node_index)];
    index_map[std::get<0>(nodes[parent(node_index)])] = node_index;
    nodes[parent(node_index)] = swap;
    index_map[std::get<0>(swap)] = parent(node_index);
    node_index = parent(node_index);
  }
}

// Return parent's node index.
template <typename ValueType>
unsigned int PriorityQueue<ValueType>::parent(unsigned int node_index) {
  return (node_index - 1) / 2;
}

// Return left child's node index.
template <typename ValueType>
unsigned int PriorityQueue<ValueType>::leftChild(unsigned int node_index) {
  return node_index * 2 + 1;
}

// Return right child's node index.
template <typename ValueType>
unsigned int PriorityQueue<ValueType>::rightChild(unsigned int node_index) {
  return node_index * 2 + 2;
}

#endif
