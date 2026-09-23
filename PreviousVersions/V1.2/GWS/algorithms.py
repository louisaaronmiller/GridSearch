import pygame
import grid
from enum import Enum
import heapq

class Node:
    def __init__(self,data):

        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        
        self.head = None

def reversalPath(path_dict,start,goal):
    current = goal # goal as key, current as value
    path = []
    while current != start:
        path.append(current)
        current = path_dict[current]
    path.reverse()
    return path


def BFS(start,goal,grid,euclidean = False, DFS = False):
    '''
    This function includes BFS and DFS, the only difference between the two 
    '''
    queue = []
    visited = set()
    queue.append(start)
    visited.add(start)
    searched = set()

    parent = {}

    while len(queue) > 0:
        if DFS:
            node = queue.pop()
        else:
            node = queue.pop(0)
        #node.searched = True
        searched.add(node)

        neighbours = grid.findNeighbours(node,euclidean)

        for row,col in neighbours:
            cell = grid.cells[row][col]

            if not cell.wall:
                if cell not in visited:
                    if cell.goal:
                        parent[cell] = node
                        return reversalPath(parent,start,goal)
                    else:
                        queue.append(cell)
                        visited.add(cell)
                        parent[cell] = node

    return reversalPath(parent,start,goal)



def BFS_initial(grid,start,goal,euclidean = False, DFS = False):
    queue = []
    visited = set()
    queue.append(start)
    visited.add(start)

    if DFS:
        node = queue.pop()
    else:
        node = queue.pop(0)

    neighbours = grid.findNeighbours(node,euclidean)

    for row,col in neighbours:
        cell = grid.cells[row][col]

        if not cell.wall:
            if cell not in visited:
                if cell.goal:
                    return queue, node, neighbours, visited
                else:
                    queue.append(cell)
                    visited.add(cell)
                    
    return queue, node, neighbours, visited


def BFS_step(queue,grid,visited,euclidean = False,DFS = False):
    if DFS:
        node = queue.pop()
    else:
        node = queue.pop(0)

    if node != grid.cells[1][1]:
        node.searched = True
    neighbours = grid.findNeighbours(node,euclidean)

    for row,col in neighbours:
            cell = grid.cells[row][col]
    
            if not cell.wall:
                if cell not in visited:
                    if cell.goal:
                        return None, None, None, None
                    else:
                        queue.append(cell)
                        visited.add(cell)
                        
    return queue, node, neighbours,visited


class Algorithm(Enum):
    BFS = 1
    DFS = 2
    DIJSTRA = 3
    ASTAR = 4
    GREEDY = 5


    names = {BFS: "Breadth First Search",
             DFS: "Depth First Search",
             DIJSTRA: "Dijstra",
             ASTAR: "A Star",
             GREEDY: "Greedy"}


def Dijstra(start,goal,grid,euclidean = False):
    '''
    This function includes BFS and DFS, the only difference between the two 
    '''
    queue = []
    visited = set()
    heapq.heappush(queue,(start.sweight,start))
    visited.add(start)
    searched = set()

    distance = {}
    distance[start] = 0

    parent = {}

    while len(queue) > 0: # could do while queue - but this is easier to read that it means when the list is not empty
        cost, node = heapq.heappop(queue)
        #node.searched = True
        searched.add(node)

        neighbours = grid.findNeighbours(node,euclidean)

        for row,col in neighbours:
            cell = grid.cells[row][col]

            if not cell.wall:
                if cell not in visited: # maybe don't add
                    if cell.goal:
                        parent[cell] = node
                        return reversalPath(parent,start,goal)
                    else:
                        new_cost = cost + cell.weight
                        if new_cost > 1: # write something that retrieves cost from dictionary and if its not there is infty
                            distance[cell] = new_cost
                            heapq.heappush(queue,(new_cost, cell))
                            visited.add(cell) # maybe remove
                            parent[cell] = node

    return reversalPath(parent,start,goal)