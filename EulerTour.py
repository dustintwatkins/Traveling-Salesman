#!/usr/bin/python3
import  copy


def set_visited(edge, edges):
    for i in range(len(edges)):
        if edges[i] == edge:
            edges[i] = (edge[0], edge[1], True)
    return edges

def EulerTour(matrix: np.ndarray):
    edges = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == float('inf') or i == j:
                continue
            edges.append((i,j, False))
    pq = []
    tours = []
    #pq contains: depth (len of path) current vertex, list of edges, current path
    for e in edges:
        path = []
        heapq.heappush(pq, (len(edges) - len(path), copy.deepcopy(e), copy.deepcopy(edges), copy.deepcopy(path)))
    while len(pq) != 0:
        current_state = heapq.heappop(pq)
        current_edge = current_state[1]
        current_edges = current_state[2]
        current_path = current_state[3]
        current_edges = set_visited(current_edge, current_edges)
        current_edge = (current_edge[0], current_edge[1], True)
        current_path.append(current_edge)
        if(len(current_path) == len(edges)):
            tours.append(current_path)
        for edge in current_edges:
            if edge[2] == True:
                continue
            if edge[0] == current_edge[1]:
                heapq.heappush(pq, (len(edges) - len(current_path), copy.deepcopy(edge), copy.deepcopy(current_edges), copy.deepcopy(current_path)))
    print('TOURS: ' + str(len(tours)))
    for t in tours:
        print('new tour')
        print(t)
    return tours
