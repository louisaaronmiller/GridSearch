import pygame
import grid
import algorithms

pygame.init()
pygame.font.init()
size_x = 1480
size_y = 960
colour = (50,48,47)
classic = grid.Grid(25,25)
grid_size_x = 900
grid_size_y = 900
wall = []

screen = pygame.display.set_mode((size_x, size_y))
                        
def drawGrid(gridX,gridY,grid,x_start = 75,y_start = 30):
    box_colour = (201, 188, 153)
    outline = (50, 48, 47)
    wall_colour = (28, 27, 27)
    start_colour = (93, 145, 71)
    goal_colour = (135, 54, 50)
    searched_colour = (131, 165, 152)#(69, 133, 136)
    frontier_colour = (8, 31, 56)
    node_colour = (87, 222, 84)

    cellX = gridX // 25
    cellY = gridY // 25

    x_spacing = x_start # these two can be seen as the top left (x,y) pixel coords
    y_spacing = y_start

    font = pygame.font.SysFont("century", 40)

    for row in range(grid.height):
        for col in range(grid.width):

            cell = grid.cells[row][col]
            
            pygame.draw.rect(screen,outline, (x_spacing - 2, y_spacing - 2, cellX + 2, cellY + 2)) # (pos_x, pos_y, size_x, size_y)

            if cell.wall:
                pygame.draw.rect(screen,wall_colour, (x_spacing, y_spacing, cellX, cellY))
            else:
                pygame.draw.rect(screen,box_colour, (x_spacing, y_spacing, cellX, cellY))

            if cell.start:

                pygame.draw.rect(screen,start_colour, (x_spacing, y_spacing, cellX, cellY))
                text_surface = font.render("S",False,(50, 48, 47))
                screen.blit(text_surface,(x_spacing + cellX //2 - 14, y_spacing + cellY //2 - 26))

            if cell.goal:

                pygame.draw.rect(screen,goal_colour, (x_spacing, y_spacing, cellX, cellY))
                text_surface = font.render("G",False,(201, 188, 153))
                screen.blit(text_surface,(x_spacing + cellX //2 - 16, y_spacing + cellY //2 - 26))

            if cell.searched:
                pygame.draw.rect(screen,searched_colour, (x_spacing, y_spacing, cellX, cellY))

            if cell.frontier:
                pygame.draw.rect(screen,frontier_colour, (x_spacing, y_spacing, cellX, cellY))

            if cell.node:
                pygame.draw.rect(screen,node_colour, (x_spacing, y_spacing, cellX, cellY))
            
            x_spacing += cellX

        x_spacing = 75
        y_spacing += cellY
    return 0

def drawPath(grid,path, x_start = 75, y_start = 30):
    cell_size = grid_size_x // 25

    box_colour = (250, 189, 47)
    outline = (50, 48, 47)

    for stone in path:
        row, col = stone.pos
        if stone.goal:
            return 0
        else:
            pygame.draw.rect(screen,outline, (x_start + cell_size * col - 2, y_start + cell_size * row - 2, cell_size + 2, cell_size + 2))
            pygame.draw.rect(screen,box_colour, (x_start + cell_size * col, y_start + cell_size * row, cell_size - 2, cell_size -2))

    return 0


def pix2ord(x,y): # short for pixel to coordinate
    cell_size = 900//25
    if x > 75 and x < 975 and y > 30 and y < 930:
        col = (x - 75) // cell_size
        row = (y - 30) // cell_size
        return row,col
    else:
        return None



classic = grid.Grid(25,25,[])
start = classic.cells[1][1]
goal = classic.cells[23][23]
path = []
result = []
current_algorithm = algorithms.Algorithm.BFS
euclidean = False
animation = True
visualise = False
DFS_bool = False

running = True
mouse_down = False
#104, 157, 106
while running:
    screen.fill(colour) #(140,148,92) <- previous sidebar colour
    pygame.draw.rect(screen,(104, 157, 106),(1055,30,350,900)) # sidebar
    pygame.draw.rect(screen, (66, 123, 88), (1055, 30, 350, 900), 8) # border

    # display text here using algorithms.Algorithm.names[current_algorithm] this will give the name of the algo

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

        if mouse_down:
            pix_x,pix_y = pygame.mouse.get_pos()
            position = pix2ord(pix_x,pix_y)

            if position is not None:
                row, col = position
                if (row, col) != (1, 1) and (row, col) != (23, 23):
                        classic.cells[row][col].wall = True

        if event.type == pygame.KEYDOWN:        
            if event.key == pygame.K_r:    # r key
                classic.gridReset()
                path = []
                visualise = False

            if event.key == pygame.K_e:       # e key
                euclidean = not euclidean
            
            if event.key == pygame.K_c:       # c key
                classic.gridClear()
                path = []
                visualise = False

            if event.key == pygame.K_1:          # 1
                current_algorithm = algorithms.Algorithm.BFS
                DFS_bool = False
            if event.key == pygame.K_2:          # 2
                DFS_bool = True

            if event.key == pygame.K_SPACE:  # space
                classic.gridClear()
                path = []
                if current_algorithm == algorithms.Algorithm.BFS:
                    if animation:
                        queue, node, neighbours, visited = algorithms.BFS_initial(classic,start,goal,euclidean,DFS_bool)
                        visualise = True
                    else:
                        path = algorithms.BFS(start,goal,classic,euclidean,DFS_bool)



    if visualise:
             for _ in range(5):
                if current_algorithm == algorithms.Algorithm.BFS:
                    result = algorithms.BFS_step(queue, classic, visited, euclidean,DFS_bool) # result is 4 values
                    if result[0] == None: # at this point all will be none, checking the first/whatever element 
                        visualise = False
                        node.node = False
                        #classic.gridReset()
                        path = []
                        path = algorithms.BFS(start,goal,classic,euclidean,DFS_bool)
                        break
                    
                    node.node = False
                    queue, node, neighbours, visited = result
                    node.node = True

                    for row in classic.cells:      # clears the entire grid of frontier
                        for cell in row:
                            cell.frontier = False

                    for cell in queue:             # makes the queue the frontier
                        cell.frontier = True


    drawGrid(grid_size_x,grid_size_y,classic)
    if path:
        #classic.gridReset()
        drawPath(classic,path)

    # draw grid here

    pygame.display.flip()

pygame.quit()

