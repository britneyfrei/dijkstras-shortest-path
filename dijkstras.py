import heapq

# creates the graph with an adjacency list
# runs Dijkstra's algorithm on the graph
# with given source and destination vertices
class Graph:

    def __init__(self):
        self.graph = {}

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, src, dest, weight):
        # need both lines since graph is undirected
        self.graph[src].append([dest, weight])
        self.graph[dest].append([src, weight])

    def dijkstra(self, src, dest):
        # keeps track of each vertex's distance from start vertex
        # initializes each distance to infinity
        distances = {vertex: float('inf') for vertex in self.graph}
        # initializes start vertex's distance to zero
        distances[src] = 0
        # keeps track of each vertex's previous vertex
        # initializes start vertex's previous vertex and weight
        # with none since it doesn't have a previous vertex
        previous = {src: (None, 0)}
        # priority queue that contains a tuple of distance and vertex
        # initializes pq with starting vertex and distance of 0
        pq = [(0, src)]
        current = 0
        while len(pq):
            # use heapq to pop the vertex with the smallest distance
            dist, current = heapq.heappop(pq)
            # once we have reached the destination vertex, leave the loop
            if current == dest:
                break
            # skip a vertex if its the current distance is greater than the one
            # that was previously determined
            if dist > distances[current]:
                continue
            # iterate through every adjacent vertex to the current one
            for edge in self.graph[current]:
                neighbor = edge[0]
                weight = edge[1]
                # calculate the distance to this neighbor
                new_dist = dist + weight
                # check if this distance is smaller than the one
                # that was previously determined
                # we only want to consider this vertex
                # if the distance is smaller
                if new_dist < distances[neighbor]:
                    # reassign distances to be the smaller distance
                    distances[neighbor] = new_dist
                    # use heapq to push the neighbor to the priority queue
                    heapq.heappush(pq, (new_dist, neighbor))
                    # also keep track of this vertex's previous
                    # vertex and distance
                    previous[neighbor] = (current, new_dist)
        # if the current is not equal to the destination
        # it means we reached the end of the graph without finding the
        # destination, so the path is not possible
        if current != dest:
            print('Path not possible.')
            quit()
        # create the path by working backwards using
        # the previous dictionary
        path = []
        while current is not None:
            path.append(current)
            # reassign current to be the previous vertex that is
            # stored in previous
            current = previous[current][0]
        # since we started with the destination and worked backwards
        # we need to reverse the path
        path = path[::-1]
        return path

def construct_graph():
    # create Graph object
    graph = Graph()
    # create a roads dictionary
    roads = {}
    # open input file for reading
    with open("Road.txt") as infile:
        # iterate through every line in the file
        for line in infile:
            # get the individual fields
            fields = line.split(',')
            a = int(fields[0])
            b = int(fields[1])
            length = float(fields[2])
            extra = fields[3].rstrip('\n')
            # use Graph class to construct graph
            graph.add_vertex(a)
            graph.add_vertex(b)
            graph.add_edge(a, b, length)
            # store the extra information and length in roads
            # using a tuple of the start and end vertices as the key
            roads[(a, b)] = (extra, length)
            roads[(b, a)] = (extra, length)
    return graph, roads

def get_IDs(src, dest):
    # create a places dictionary
    places = {}
    # open the input file for reading
    with open("Place.txt") as infile:
        # iterate through each line in the file
        for line in infile:
            # get the individual fields
            fields = line.split(',')
            placeID = int(fields[0])
            name = fields[1].rstrip('\n')
            # get the IDs of the given source and destination names
            if name == src:
                src = placeID
            if name == dest:
                dest = placeID
            # store the name in places using the ID as the key
            places[placeID] = name
    return src, dest, places

def print_path(path, roads, places):
    # keep track of total miles in path
    total = 0
    # iterate through the path
    for i in range(len(path)-1):
        # check that the ID has a name, otherwise give the name null
        if not path[i] in places:
            first_place = 'null'
        else:
            first_place = places[path[i]]
        if not path[i+1] in places:
            second_place = 'null'
        else:
            second_place = places[path[i+1]]
        # formatted print
        print(f'\t{i+1}. {path[i]}({first_place}) -> {path[i+1]}({second_place}), {roads[(path[i], path[i+1])][0]}, {roads[(path[i], path[i+1])][1]} mi.')
        total += roads[(path[i], path[i+1])][1]
    return total

def main():
    # get input from user
    source = input("Enter the Source name:\n")
    dest = input("Enter Destination name:\n")
    graph, roads = construct_graph()
    # convert given names to their IDs
    sourceID, destID, places = get_IDs(source, dest)
    # get shortest path using dijkstra()
    path = graph.dijkstra(sourceID, destID)
    # formatted print
    print(f'Searching from {sourceID}({source}) to {destID}({dest})')
    total = print_path(path, roads, places)
    print(f'It takes {"{:.2f}".format(total)} miles from {sourceID}({source}) to {destID}({dest}).')


if __name__ == '__main__':
    main()
