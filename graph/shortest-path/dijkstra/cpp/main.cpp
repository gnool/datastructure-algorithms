#include <iostream>
#include <fstream>
#include <time.h>
#include "simulator.h"

using namespace std;

int main() {
  srand(time(0));  // for seeding the Mersenne Twister
  filebuf fb;
  fb.open ("dijkstra_output.txt",ios::out);
  ostream os(&fb);
  // For density = 0.2
  Simulator sim(50, 0.2, 1.0, 10.0);
  os << "Simulating graph..." << endl;
  os << "> Total nodes:         50" << endl;
  os << "> Density:             0.2" << endl;
  os << "> Minimum edge weight: 1.0" << endl;
  os << "> Maximum edge weight: 10.0" << endl << endl;
  os << sim.graph() << endl;
  os << sim.path() << endl;
  // For density = 0.4
  Simulator sim2(50, 0.4, 1.0, 10.0);
  os << "Simulating graph..." << endl;
  os << "> Total nodes:         50" << endl;
  os << "> Density:             0.4" << endl;
  os << "> Minimum edge weight: 1.0" << endl;
  os << "> Maximum edge weight: 10.0" << endl << endl;
  os << sim2.graph() << endl;
  os << sim2.path() << endl;
  os << "Gathering statistics..." << endl;
  os << "Average path length (density=0.2) over 10000 random graphs: " << sim.calcAveragePathLength(10000) << endl;
  os << "Average path length (density=0.4) over 10000 random graphs: " << sim2.calcAveragePathLength(10000) << endl;
  fb.close();
  return 0;
}
