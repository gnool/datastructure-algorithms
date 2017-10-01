#include <iostream>
#include <time.h>
#include "simulator.h"

using namespace std;

int main() {
  srand(time(0));  // for seeding the Mersenne Twister
  // For density = 0.2
  Simulator sim(5000, 0.2, 1.0, 10.0);
  cout << "Average path length (50 nodes, 0.2 density, 1.0 min edge weight and "
       << "10.0 max edge weight): " << sim.calcAveragePathLength(1) << endl;
  // For density = 0.4
  Simulator sim2(5000, 0.4, 1.0, 10.0);
  cout << "Average path length (50 nodes, 0.4 density, 1.0 min edge weight and "
       << "10.0 max edge weight): " << sim2.calcAveragePathLength(1) << endl;
  return 0;
}