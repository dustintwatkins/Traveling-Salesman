#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq

#Time Complexity: O(n)
def reduce_row(matrix, row):
    min_val = min(matrix[row])
    if min_val == float('inf'):                                 #float('inf') - float('inf') = NaN
        return 0;
    for i in range(len(matrix)):
        matrix[row][i] -= min_val
    return min_val

#Time Complexity: O(n^2)
#Space Complexity: O(n)
def reduce_col(matrix, col):
    lst = []
    #Time Complexity: O(n)
    for i in range(len(matrix)):
        lst.append(matrix[i][col])

    min_val = min(lst)

    if min_val == float('inf'):                                 #float('inf') - float('inf') = NaN
        return 0;

    #Time Complexity: O(n)
    for x in range(len(matrix)):
        matrix[x][col] -= min_val

    return min_val

#Time Complexity: O(n)
def set_row(matrix, row, value):
    for i in range(len(matrix)):
        matrix[row][i] = value

#Time Complexity: O(n)
def set_col(matrix, col, value):
    for i in range(len(matrix)):
        matrix[i][col] = value

#Time Complexity: O(n)
def reduce_matrix(matrix):
    lb = 0
    for i in range(len(matrix)):
        lb = lb + reduce_row(matrix, i)
    for j in range(len(matrix)):
        lb = lb + reduce_col(matrix, j)
    return lb

class TSPSolver:
    def __init__( self, gui_view ):
        self._scenario = None

    def setupWithScenario( self, scenario ):
        self._scenario = scenario


    ''' <summary>
        This is the entry point for the default solver
        which just finds a valid random tour
        </summary>
        <returns>results array for GUI that contains three ints: cost of solution, time spent to find solution, number of solutions found during search (
not counting initial BSSF estimate)</returns> '''
    def defaultRandomTour( self, start_time, time_allowance=60.0 ):

        results = {}

        start_time = time.time()

        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        while not foundTour:
            # create a random permutation
            perm = np.random.permutation( ncities )

            #for i in range( ncities ):
                #swap = i
                #while swap == i:
                    #swap = np.random.randint(ncities)
                #temp = perm[i]
                #perm[i] = perm[swap]
                #perm[swap] = temp

            route = []

            # Now build the route using the random permutation
            for i in range( ncities ):
                route.append( cities[ perm[i] ] )

            bssf = TSPSolution(route)
            #bssf_cost = bssf.cost()
            #count++;
            count += 1

            #if costOfBssf() < float('inf'):
            if bssf.costOfRoute() < np.inf:
                # Found a valid route
                foundTour = True
        #} while (costOfBssf() == double.PositiveInfinity);                // until a valid route is found
        #timer.Stop();

        results['cost'] = bssf.costOfRoute() #costOfBssf().ToString();                          // load results array
        results['time'] = time.time() - start_time
        results['count'] = count
        results['soln'] = bssf

       # return results;
        return results



    def greedy( self, start_time, time_allowance=60.0 ):
        pass

    def branchAndBound( self, start_time, time_allowance=60.0 ):
        start_time = time.time()
        cities = self._scenario.getCities()
        ncities = len(cities)

        #Space Complexity: O(n^2)
        initial_matrix = np.arange(float(ncities**2)).reshape(ncities, ncities)

        #Time Complexity: O(n^2)
        for i in range(ncities):
            for j in range(ncities):
                initial_matrix[i][j] = cities[i].costTo(cities[j])

        initial_results = self.defaultRandomTour(start_time, 60)
        bssf = {}
        bssf['cost'] = initial_results['cost']
        bssf['time'] = initial_results['time']
        bssf['count'] = 1
        bssf['soln'] = initial_results['soln']

        lower_bound = reduce_matrix(initial_matrix)

        pq = []

        #Space Complexity: O(1)
        heapq.heappush(pq, (len(cities) - 1, lower_bound, [0], initial_matrix))
        states_pruned = 0
        states_created = 1
        max_heap_size = len(pq)

        #Time Complexity:
        #Space Complexity:
        while(len(pq) != 0 and time.time() - start_time < 60):
            #Time Complexity: O(1)
            state  = heapq.heappop(pq)
            curr_depth = len(cities) - state[0]
            lb = state[1]
            visited = state[2]
            matrix = state[3]

            if curr_depth == len(cities):                                #reached leaf node
                if lb < bssf['cost']:                                   #if better than BSSF
                    bssf['cost'] = lb
                    bssf['soln'] = []

                    #Time Complexity: O(n)
                    for i in visited:
                        bssf['soln'].append(cities[i])
                    bssf['soln'] = TSPSolution(bssf['soln'])
                    bssf['cost'] = bssf['soln'].costOfRoute()
                    bssf['count'] += 1
                continue

            #Time Complexity: O(n)
            #Space Complexity: O(n^2)
            for i in range(1, ncities):
                temp_lb = lb
                if matrix[visited[len(visited) - 1]][i] != float('inf'): #Look for valid cities to visit
                    states_created += 1
                    #Space Complexity: O(n)
                    cpy_matrix = np.array(matrix)
                    temp_lb += cpy_matrix[visited[len(visited) - 1]][i]
                    set_row(cpy_matrix, visited[len(visited) - 1], float('inf'))
                    set_col(cpy_matrix, i, float('inf'))
                    cpy_matrix[i][visited[len(visited) -1]] = float('inf')
                    temp_lb += reduce_matrix(cpy_matrix)
                    if temp_lb < bssf['cost']:                          #State was not pruned
                        new_visited = list(visited)
                        new_visited.append(i)

                        #Space Complexity: O(1)
                        heapq.heappush(pq, (len(cities)- curr_depth - 1, temp_lb, new_visited, cpy_matrix))
                        if max_heap_size < len(pq):                      #check heap size
                            max_heap_size = len(pq)
                    else:                                                #State was pruned
                        states_pruned += 1

            bssf['time'] = time.time() - start_time

        print("=======================================")
        print('states created: ' + str(states_created))
        print('states pruned: ' + str(states_pruned))
        print('max heap size: ' + str(max_heap_size))
        return bssf


    def fancy( self, start_time, time_allowance=60.0 ):
        pass
