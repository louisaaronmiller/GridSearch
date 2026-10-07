import pygame
import grid
from enum import Enum
import heapq
import itertools
from random import randrange
import random
import math

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
    counter = 0 
    if DFS:
        node = queue.pop()
    else:
        node = queue.pop(0)

    if node != grid.cells[1][1]:
        node.searched = True
        counter += 1
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
                        
    return queue, node, neighbours,visited,counter


class Algorithm(Enum):
    BFS = 1
    DFS = 2
    DIJSTRA = 3
    ASTAR = 4
    GREEDY = 5


algoNames = {Algorithm.BFS: "Breadth First Search",
            Algorithm.DFS: "Depth First Search",
            Algorithm.DIJSTRA: "Dijkstra",
            Algorithm.ASTAR: "A Star",
            Algorithm.GREEDY: "Greedy Best-First"}

algoText = {Algorithm.BFS: "Searches each available node one \n distance layer at a time",
            Algorithm.DFS: "Searches deep as possible before \n backtracking to the next node",
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
                        if new_cost < distance.get(cell, float("inf")): # retrieves smallest cost from start to that cell and if its not there returns infty
                            distance[cell] = new_cost
                            heapq.heappush(queue,(new_cost,cell.row, cell.col, cell))
                            #visited.add(cell) # maybe remove
                            parent[cell] = node

    return reversalPath(parent,start,goal)


# Algorithm descriptions
bfs_desc = ['Searches each available node using ', 'a queue one distance layer at a time']
dfs_desc = ["Searches deep as possible with a stack", "before backtracking to the next node"]
dijkstra_desc = ['Searches the lowest cost node using', 'the total path cost']
astar_desc = ['Searches the most promising node using ', 'path cost and distance to the goal']
greedy_desc = ['Searches the closest node to the goal ', 'using only estimated distance']

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



def mazeGeneration(grid,euclidean):
    '''
    DFS maze generation
    '''

    grid.allWalls() # makes all cells walls
    rand_row = randrange(grid.height) # generates random integer number between 0 and grid.height
    rand_col = randrange(grid.width)
    visited = set()

    looping_cell = grid.cells[rand_row][rand_col]
    visited.add(looping_cell)

    unvisited = []
    stack = []
    stack.append(looping_cell)

    visited.add(grid.cells[1][1])
    visited.add(grid.cells[23][23])

    while stack:
        #neighbours = grid.findNeighbours(looping_cell,euclidean)
        neighbours = grid.findMazeNeighbours(looping_cell,euclidean)
        
        for row,col in neighbours:
            cell = grid.cells[row][col]
            if cell not in visited:
                unvisited.append(cell)

        if unvisited:

            stack.append(looping_cell)
        
            random_unvisited_cell = random.choice(unvisited)
            looping_cell.wall = False
            random_unvisited_cell.wall = False

            middle_row = (looping_cell.row + random_unvisited_cell.row) // 2
            middle_col = (looping_cell.col + random_unvisited_cell.col) // 2

            grid.cells[middle_row][middle_col].wall = False

            looping_cell = random_unvisited_cell
            visited.add(looping_cell)

        else:
            if stack:
                looping_cell = stack.pop() # if there is no elements within univisited we check the last cell

        unvisited = []


def astar(start,goal,grid,euclidean = False,heuristic = "man"):
    queue = []
    visited = set()
    if heuristic == "man":
        f_cost = 0 + 43 # distance to goal
    elif heuristic == "euc":
        f_cost = 0 + 21 # distance to goal

    heapq.heappush(queue,(f_cost, grid.sweight,start))
    visited.add(start)
    searched = set()

    distance = {}
    distance[start] = grid.sweight

    parent = {}

    while len(queue) > 0: # could do while queue - but this is easier to read that it means when the list is not empty
        f,cost ,node = heapq.heappop(queue)
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
                        if new_cost < distance.get(cell, float("inf")): # retrieves smallest cost from start to that cell and if its not there returns infty
                            distance[cell] = new_cost
                            parent[cell] = node
                            if heuristic == "man":
                                h = abs(cell.row - goal.row) + abs(cell.col - goal.col)
                            elif heuristic == "euc":
                                h = math.sqrt((cell.row - goal.row)**2 + (cell.col - goal.col)**2 )
                                
                            f = new_cost + h
                            
                            heapq.heappush(queue,(f,new_cost, cell))
                            #visited.add(cell) # maybe remove

    return reversalPath(parent,start,goal)