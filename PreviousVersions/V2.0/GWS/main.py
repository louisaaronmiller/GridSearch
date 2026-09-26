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
    weight_colour = (158, 147, 117)
    outline_colour = (50, 48, 47)
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
    font_weights = pygame.font.SysFont("lato", 40)

    for row in range(grid.height):
        for col in range(grid.width):

            cell = grid.cells[row][col]
            
            pygame.draw.rect(screen,outline_colour, (x_spacing - 2, y_spacing - 2, cellX + 2, cellY + 2)) # (pos_x, pos_y, size_x, size_y)

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

            if cell.weight > 1:
                pygame.draw.rect(screen,weight_colour, (x_spacing, y_spacing, cellX, cellY))
                text_surface_weight = font_weights.render(f"{cell.weight}",True, outline_colour)
                screen.blit(text_surface_weight,(x_spacing + cellX //2 - 9, y_spacing + cellY //2 - 14))

            if cell.searched:
                pygame.draw.rect(screen,searched_colour, (x_spacing, y_spacing, cellX, cellY))
                if cell.weight > 1:
                    text_surface_weight = font_weights.render(f"{cell.weight}",True, outline_colour)
                    screen.blit(text_surface_weight,(x_spacing + cellX //2 - 9, y_spacing + cellY //2 - 14))

            if cell.frontier:
                pygame.draw.rect(screen,frontier_colour, (x_spacing, y_spacing, cellX, cellY))
                if cell.weight > 1:
                    text_surface_weight = font_weights.render(f"{cell.weight}",True, outline_colour)
                    screen.blit(text_surface_weight,(x_spacing + cellX //2 - 9, y_spacing + cellY //2 - 14))

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
    outline_colour = (50, 48, 47)

    font_weights = pygame.font.SysFont("lato", 40)

    for stone in path:
        row, col = stone.pos
        if stone.goal: # doesn't draw on goal cell
            return 0
        else:
                pygame.draw.rect(
                screen,outline,
                (x_start + cell_size * col - 2,
                y_start + cell_size * row - 2,
                cell_size + 2, cell_size + 2))

                pygame.draw.rect(
                screen,box_colour, 
                (x_start + cell_size * col,
                y_start + cell_size * row,
                cell_size - 2, cell_size -2))

                if stone.weight > 1:
                    text_surface_weight = font_weights.render(f"{stone.weight}",True, outline_colour)
                    screen.blit(text_surface_weight,(x_start + cell_size * col + cell_size //2 - 9,
                                                     y_start + cell_size * row + cell_size //2 - 14))

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
counter = 0
counter_to_print = 0
distance = []
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
    #pygame.draw.rect(screen,(104, 157, 106),(1055,30,350,900)) # sidebar

    #region - Drawing stuff
    box_colour = (201, 188, 153)
    weight_colour = (158, 147, 117)
    outline_colour = (50, 48, 47)
    wall_colour = (28, 27, 27)
    start_colour = (93, 145, 71)
    goal_colour = (135, 54, 50)
    searched_colour = (131, 165, 152)#(69, 133, 136)
    frontier_colour = (8, 31, 56)
    node_colour = (87, 222, 84)
    path_colour = (250, 189, 47)



    sidebar_font = pygame.font.SysFont("lato", 80)
    algo_text_font = pygame.font.SysFont("lato", 40)
    normal_text_font = pygame.font.SysFont("lato", 25)

    sidebar = pygame.Surface((350,900))
    sidebar.fill((104, 157, 106))

    title_text = sidebar_font.render(f"Grid Search", True, (50, 48, 47))
    algo_text = algo_text_font.render(f"{algorithms.algoNames[current_algorithm]}", True, outline_colour)
    sidebar.blit(title_text,(17,20))
    sidebar.blit(algo_text,(22,75))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 349, 14, 14))
    legend_start = pygame.draw.rect(sidebar,start_colour, (22, 350, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 369, 14, 14))
    legend_start = pygame.draw.rect(sidebar,goal_colour, (22, 370, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 389, 14, 14))
    legend_start = pygame.draw.rect(sidebar,wall_colour, (22, 390, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 409, 14, 14))
    legend_start = pygame.draw.rect(sidebar,searched_colour, (22, 410, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 429, 14, 14))
    legend_start = pygame.draw.rect(sidebar,frontier_colour, (22, 430, 12, 12)) 

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 449, 14, 14))
    legend_start = pygame.draw.rect(sidebar,node_colour, (22, 450, 12, 12))


    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 469, 14, 14))
    legend_weight_font = pygame.font.SysFont("lato",22)
    legend_weight_text = legend_weight_font.render("x", True,outline_colour)
    legend_start = pygame.draw.rect(sidebar,weight_colour, (22, 470, 12, 12))
    sidebar.blit(legend_weight_text, (24, 468))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 489, 14, 14))
    legend_start = pygame.draw.rect(sidebar,path_colour, (22, 490, 12, 12))

    legend_start_text = normal_text_font.render("Start cell", True, outline_colour)
    legend_goal_text = normal_text_font.render("Goal cell", True, outline_colour)
    legend_wall_text = normal_text_font.render("Wall", True, outline_colour)
    legend_searched_text = normal_text_font.render("Searched cell", True, outline_colour)
    legend_frontier_text = normal_text_font.render("Frontier cell", True, outline_colour)
    legend_node_text = normal_text_font.render("Node", True, outline_colour)
    legend_weighted_text = normal_text_font.render("Weighted cell", True, outline_colour)
    legend_shortestpath_text = normal_text_font.render("Shortest path", True, outline_colour)

    sidebar.blit(legend_start_text,(40,348))
    sidebar.blit(legend_goal_text,(40,368))
    sidebar.blit(legend_wall_text,(40,388))
    sidebar.blit(legend_searched_text,(40,408))
    sidebar.blit(legend_frontier_text,(40,428))
    sidebar.blit(legend_node_text,(40,448))
    sidebar.blit(legend_weighted_text,(40,468))
    sidebar.blit(legend_shortestpath_text,(40,488))

    #endregion - Drawing stuff

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
                counter_to_print = 0

            if event.key == pygame.K_e:       # e key
                euclidean = not euclidean
            
            if event.key == pygame.K_c:       # c key
                classic.gridClear()
                path = []
                visualise = False
                counter_to_print = 0

            if event.key == pygame.K_w:       # w key
                #classic.gridClear()
                path = []
                #visualise = False

                classic.giveWeights()

            if event.key == pygame.K_1:          # 1
                current_algorithm = algorithms.Algorithm.BFS
                DFS_bool = False
                classic.gridClear()
                counter_to_print = 0
                path = []
                visualise = False
            if event.key == pygame.K_2:         # 2
                current_algorithm = algorithms.Algorithm.DFS
                DFS_bool = True
                counter_to_print = 0
                classic.gridClear()
                path = []
                visualise = False
            if event.key == pygame.K_3:          # 3
                current_algorithm = algorithms.Algorithm.DIJSTRA
                classic.gridClear()
                path = []
                visualise = False


            if event.key == pygame.K_SPACE:  # space
                classic.gridClear()
                path = []
                if current_algorithm == algorithms.Algorithm.BFS or current_algorithm == algorithms.Algorithm.DFS:
                    if animation:
                        queue, node, neighbours, visited = algorithms.BFS_initial(classic,start,goal,euclidean,DFS_bool)
                        visualise = True
                    else:
                        path = algorithms.BFS(start,goal,classic,euclidean,DFS_bool)

                if current_algorithm == algorithms.Algorithm.DIJSTRA:
                    if animation:
                        nodes, queue, counter, node, neighbours, distance = algorithms.Dijstra_init(start,goal,classic,euclidean)
                        visualise= True
                    else:
                        path = algorithms.Dijstra(start,goal,classic,euclidean)




    if visualise:
             for _ in range(5):
                if current_algorithm == algorithms.Algorithm.BFS or current_algorithm == algorithms.Algorithm.DFS:
                    result = algorithms.BFS_step(queue, classic, visited, euclidean,DFS_bool) # result is 4 values
                    if result[0] == None: # at this point all will be none, checking the first/whatever element 
                        visualise = False
                        node.node = False
                        #classic.gridReset()
                        path = []
                        path = algorithms.BFS(start,goal,classic,euclidean,DFS_bool)
                        break
                    
                    node.node = False # for drawing
                    queue, node, neighbours, visited = result
                    node.node = True

                if current_algorithm == algorithms.Algorithm.DIJSTRA:
                    result = algorithms.Dijstra_step(queue,counter,distance,classic,euclidean)
                    if result[0] == None: 
                        visualise = False
                        node.node = False
                        #classic.gridReset()
                        path = []
                        path = algorithms.Dijstra(start,goal,classic,euclidean)
                        break 

                    node.node = False # for drawing
                    nodes,queue, node, neighbours, distance, counter_to_print = result
                    node.node = True

                for row in classic.cells:      # clears the entire grid of frontier
                    for cell in row:
                        cell.frontier = False

                if current_algorithm == algorithms.Algorithm.DIJSTRA:
                    for cell in nodes:
                        cell.frontier = True
                else:
                    for cell in queue:
                        cell.frontier = True

                

                    




    count_text = normal_text_font.render(f"Live {counter_to_print}", True, (50, 48, 47))
    sidebar.blit(count_text, (23,300))

    screen.blit(sidebar,(1055,30))
    pygame.draw.rect(screen, (66, 123, 88), (1055, 30, 350, 900), 8) # border
    drawGrid(grid_size_x,grid_size_y,classic)
    if path:
        #classic.gridReset()
        drawPath(classic,path)

    # draw grid here

    pygame.display.flip()

pygame.quit()

