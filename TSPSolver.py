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

    def reduce_row(matrix, row):
        min_val = min(matrix[row])
        for i in range(len(matrix)):
            matrix[row][i] -= min_val
        return min_val

    def reduce_col(matrix, col):
        lst = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if j == col:
                    lst.append(matrix[i][j])
        min_val = min(lst)
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                if y == col:
                    matrix[x][y] -= min_val
        return min_val

    def set_row(matrix, row, value):
        for i in range(len(matrix)):
            matrix[row][i] = value

    def set_col(matrix, col, value):
        for i in range(len(matrix)):
            matrix[i][col] = value

    def reduce_matrix(matrix):
        lb = 0
        for i in range(len(matrix)):
            lb = lb + reduce_row(matrix, i)
        for j in range(len(matrix)):
            lb = lb + reduce_col(matrix, j)
        return lb

    def branchAndBound( self, start_time, time_allowance=60.0 ):
        cities = self._scenario.getCities()
        ncities = len(cities)
        initial_matrix = np.arange(ncities**2).reshape(ncities, ncities)

        initial_results = defaultRandomTour(self, start_time, 60)
        bssf = results['cost']

        for i in range(ncities):
            for j in range(ncities):
                if i == j:
                    initial_matrix[i][j] = float.('inf')
                    continue
                initial_matrix[i][j] = cities[i].costTo(cities[j])





    def fancy( self, start_time, time_allowance=60.0 ):
        pass
