#!/usr/bin/python3

def set_visited(edge, edges):
    for i in range(len(edges)):
        if edges[i] == edge:
            edges[i] = (edge[0], edge[1], True)
    return edges

def EulerTour(matrix):
    edges = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == float('inf') or i == j:
                continue
            edges.append((i,j, False))
    pq = []
    path = []
    tours = []
    #q contains: depth (len of path) current vertex, list of edges, current path
    heapq.heappush(pq, (len(edges) - len(path), edges[0], edges, path))
    while len(pq) != 0:
        print("entered")
        current_state = heapq.heappop(pq)
        print('STATE')
        print(current_state)
        current_edge = current_state[1]
        current_edges = current_state[2]
        current_path = current_state[3]
        current_edges = set_visited(current_edge, current_edges)
        print('edges')
        print(current_edges)
        current_edge = (current_edge[0], current_edge[1], True)
        print('edge')
        print(current_edge)
        current_path.append(current_edge)
        print('path')
        print(current_path)
        if(len(current_path) == len(edges)):
            print("FOUND")
            tours.append(current_path)
        for edge in current_edges:
            print("for")
            if edge[2] == True:
                continue
            if edge[0] == current_edge[1]:
                print('size: ' + str(len(pq)))
                print('adding')
                print(edge)
                heapq.heappush(pq, (len(edges) - len(current_path), edge, current_edges, current_path))
    print('TOURS: ' + str(len(tours)))
    return tours
