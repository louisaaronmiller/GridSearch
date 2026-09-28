import pygame
import grid
from enum import Enum
import heapq
import itertools

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


algoNames = {Algorithm.BFS: "Breadth First Search",
            Algorithm.DFS: "Depth First Search",
            Algorithm.DIJSTRA: "Dijstra",
            Algorithm.ASTAR: "A Star",
            Algorithm.GREEDY: "Greedy"}

algoText = {Algorithm.BFS: "Searches each available node one \n distance layer at a time",
            Algorithm.DFS: "Searches deep as possible before \m backtracking to the next node",
            Algorithm.DIJSTRA: "x",
            Algorithm.ASTAR: "y",
            Algorithm.GREEDY: "z"}


def Dijstra(start,goal,grid,euclidean = False):
    queue = []
    visited = set()
    heapq.heappush(queue,(grid.sweight,1,1,start))
    visited.add(start)
    searched = set()

    distance = {}
    distance[start] = grid.sweight

    parent = {}

    while len(queue) > 0: # could do while queue - but this is easier to read that it means when the list is not empty
        cost, row, col,node = heapq.heappop(queue)
        #node.searched = True
        searched.add(node)

        neighbours = grid.findNeighbours(node,euclidean)

        for row,col in neighbours:
            cell = grid.cells[row][col]

            if not cell.wall:
                #if cell not in visited: # maybe don't add
                    if cell.goal:
                        parent[cell] = node
                        return reversalPath(parent,start,goal)
                    else:
                        new_cost = cost + cell.weight
                        if new_cost < distance.get(cell, float("inf")): # write something that retrieves cost from dictionary and if its not there is infty
                            distance[cell] = new_cost
                            heapq.heappush(queue,(new_cost,cell.row, cell.col, cell))
                            #visited.add(cell) # maybe remove
                            parent[cell] = node

    return reversalPath(parent,start,goal)





def Dijstra_init(start,goal,grid,euclidean = False):
    queue = []
    visited = set()

    counter = itertools.count()

    heapq.heappush(queue,(grid.sweight,next(counter),start))
    visited.add(start)
    searched = set()

    distance = {}
    distance[start] = grid.sweight

    parent = {}

    cost, _, node = heapq.heappop(queue)
    #node.searched = True
    searched.add(node)

    neighbours = grid.findNeighbours(node,euclidean)

    for row,col in neighbours:
        cell = grid.cells[row][col]

        if not cell.wall:
            #if cell not in visited: # maybe don't add
                if cell.goal:
                    parent[cell] = node
                    return reversalPath(parent,start,goal)
                else:
                    new_cost = cost + cell.weight
                    if new_cost < distance.get(cell, float("inf")): # write something that retrieves cost from dictionary and if its not there is infty
                        distance[cell] = new_cost
                        heapq.heappush(queue,(new_cost,next(counter),cell))
                        #visited.add(cell) # maybe remove
                        parent[cell] = node

    nodes = [entry[2] for entry in queue]

    return nodes, queue, counter, node, neighbours, distance


def Dijstra_step(queue,counter,distance,grid,euclidean=False):

    cost, _, node = heapq.heappop(queue)
    node.searched = True

    neighbours = grid.findNeighbours(node,euclidean)

    for row,col in neighbours:
        cell = grid.cells[row][col]

        if not cell.wall:
                if cell.goal:
                    return None, None,None,None
                else:
                    new_cost = cost + cell.weight
                    if new_cost < distance.get(cell, float("inf")):
                        distance[cell] = new_cost
                        heapq.heappush(queue,(new_cost,next(counter),cell))
                        #visited.add(cell) # maybe remove
    nodes = []
    for i in queue:
        nodes.append(i[2])
        i[2].searched = True

    return nodes,queue, node, neighbours, distance,counter # a bit confusing but the "queue" as its used above is nodes