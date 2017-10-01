all: dijkstra.exe
	rm main.o
	rm simulator.o
	rm shortest_path.o
	rm graph.o

dijkstra.exe: main.o simulator.o shortest_path.o graph.o
	g++ -o dijkstra.exe main.o simulator.o shortest_path.o graph.o -Wall -std=gnu++11

main.o: main.cpp
	g++ -c main.cpp -Wall -std=gnu++11

simulator.o: simulator.cpp
	g++ -c simulator.cpp -Wall -std=gnu++11

shortest_path.o: shortest_path.cpp
	g++ -c shortest_path.cpp -Wall -std=gnu++11

graph.o: graph.cpp
	g++ -c graph.cpp -Wall -std=gnu++11

clean:
	rm main.o
	rm simulator.o
	rm shortest_path.o
	rm graph.o