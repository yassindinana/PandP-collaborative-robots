import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

##############################################################################
# heuristic function for path scoring
##############################################################################

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


##############################################################################
# path finding function
##############################################################################

def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:      #Loop until current == goal
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        # if goal not reached yet
        #Add current point to close_set for comparison
        close_set.add(current)
        for i, j in neighbors:     #Loop on neighbours
            neighbor = current[0] + i, current[1] + j     #Get the neighbour point
            tentative_g_score = gscore[current] + heuristic(current, neighbor)      #Calculate the new score
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                #array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False



def a_star_compute(grid,start, goal):
    route = astar(grid, start, goal)
    route = route + [start]
    route = route[::-1]
    print(route)

    ##############################################################################
    # plot the path
    ##############################################################################

    # extract x and y coordinates from route list
    x_coords = []
    y_coords = []

    for i in (range(0, len(route))):
        x = route[i][0]
        y = route[i][1]
        x_coords.append(x)
        y_coords.append(y)

    return x_coords , y_coords




