import pygame
import grid
from enum import Enum

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


def BFS(start,goal,grid,euclidean = False):
    '''
    at the minute the function arguments are slightly redundant,
    this is beccause start and goal are hardcoded into the grid
    at the moment, therefore, passing them in the function
    doesn't do anything, the function will use it.
    '''
    queue = []
    visited = set()
    queue.append(start)
    visited.add(start)
    searched = set()

    parent = {}

    while len(queue) > 0:
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



def BFS_initial(grid,start,goal,euclidean = False):
    queue = []
    visited = set()
    queue.append(start)
    visited.add(start)

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


def BFS_step(queue,grid,visited,euclidean = False):
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



