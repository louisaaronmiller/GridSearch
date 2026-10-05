import pygame
import random

class Cell:
    def __init__(self,row, col, wall = False, weight = 1, start = False, goal = False, searched = False, 
                 frontier = False,
                 node = False):

        self.row = row
        self.col = col
        self.wall = wall
        self.weight = weight
        self.start = start
        self.goal = goal
        self.pos = row,col
        self.searched = searched
        self.frontier = frontier
        self.node = node

class Grid:
    def __init__(self,
                height: int,
                width: int,
                walls = []) -> None:

        self.height = height
        self.width = width
        self.sweight = 0 # start weight
        self.gweight = 0 # goal weight
        cells = []

        for i in range(self.height):
            row = []
            for j in range(self.width):

                row.append(Cell(i,j))
            cells.append(row.copy())
            row.clear()

        
        if len(walls) != 0:
            for row,col in walls:
                cells[row][col] = Cell(row,col,True)

        cells[1][1] = Cell(1,1,False,0,True) # start block
        cells[23][23] = Cell(23,23,False,0,False,True) # end block

        self.cells = cells

    def gridReset(self): # resets everything
        for row in range(self.height):
            for col in range(self.width):
                self.cells[row][col].wall = False
                self.cells[row][col].searched = False
                self.cells[row][col].frontier = False
                self.cells[row][col].node = False
                self.cells[row][col].weight = 1

        self.cells[1][1].weight = 0
        self.cells[23][23].weight = 0 # resets the start/end block

    def gridClear(self): # keeps walls and weights
        for row in range(self.height):
            for col in range(self.width):
                self.cells[row][col].searched = False
                self.cells[row][col].node = False
                self.cells[row][col].frontier = False


    def findNeighbours(self,point,euclidean = False):
        '''
        return: up,down,left,right
        '''
        row = point.row
        col = point.col

        if euclidean:
            down = (row + 1, col)
            up = (row - 1, col)
            left = (row, col -1)
            right = (row, col + 1)
            top_right = (row - 1, col + 1)
            top_left = (row - 1, col -1)
            bottom_right = (row + 1, col + 1)
            bottom_left = (row + 1, col -1)

            array = [down, up, left, right,top_left,top_right, bottom_left, bottom_right]
            valid = []
    
            for row, col in array:
                if 0 <= row < self.height and 0 <= col < self.width:
                    valid.append((row, col))
        else:
        
            down = (row + 1, col)
            up = (row - 1, col)
            left = (row, col -1)
            right = (row, col + 1)

            array = [down, up, left, right]
            valid = []

            for row, col in array:
                if 0 <= row < self.height and 0 <= col < self.width:
                    valid.append((row, col))

        return tuple(valid)

    def findMazeNeighbours(self,point,euclidean = False):
        '''
        return: up,down,left,right
        '''
        row = point.row
        col = point.col

        if euclidean:
            down = (row + 2, col)
            up = (row - 2, col)
            left = (row, col -2)
            right = (row, col + 2)
            top_right = (row - 2, col + 2)
            top_left = (row - 2, col -2)
            bottom_right = (row + 2, col + 2)
            bottom_left = (row + 2, col -2)

            array = [down, up, left, right,top_left,top_right, bottom_left, bottom_right]
            valid = []
    
            for row, col in array:
                if 0 <= row < self.height and 0 <= col < self.width:
                    valid.append((row, col))
        else:
        
            down = (row + 2, col)
            up = (row - 2, col)
            left = (row, col -2)
            right = (row, col + 2)

            array = [down, up, left, right]
            valid = []

            for row, col in array:
                if 0 <= row < self.height and 0 <= col < self.width:
                    valid.append((row, col))

        return tuple(valid)

    def giveWeights(self):
        weights = [2,3,4,5]
        for row in range(self.height):
            for col in range(self.width):
                cell = self.cells[row][col]
                if random.uniform(0,1) > 0.92: # 8% chance
                    if not cell.wall: # if wall skip
                        cell.weight = random.choice(weights)
        self.cells[1][1].weight = 0
        self.cells[23][23].weight = 0

    def weightCount(self):
        count = 0 
        total_weight = 0
        for row in range(self.height):
            for col in range(self.width):
                cell = self.cells[row][col]
                if cell.weight > 1:
                    count += 1
                    total_weight += cell.weight
                else:
                    total_weight += cell.weight

        return count, total_weight

    def allWalls(self):
        for row in range(self.height):
            for col in range(self.width):
                cell = self.cells[row][col]
                if row == 1 and col == 1:
                    continue
                if row == 23 and col == 23:
                    continue
                    
                cell.wall = True

    









    





