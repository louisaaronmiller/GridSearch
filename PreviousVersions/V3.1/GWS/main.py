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
            return len(path) - 1 # this doesn't include GOAL/START (hence the -1)
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

    return len(path) -1 # this doesn't include GOAL/START (hence the -1)


def pix2ord(x,y): # short for pixel to coordinate
    cell_size = 900//25
    if x > 75 and x < 975 and y > 30 and y < 930:
        col = (x - 75) // cell_size
        row = (y - 30) // cell_size
        return row,col
    else:
        return None

def pathCount(path):
    count = 0
    for cell in path:
        count += cell.weight
    return count # this doesn't include GOAL/START since they are weight = 0 




classic = grid.Grid(25,25,[])
start = classic.cells[1][1]
goal = classic.cells[23][23]
path = []
result = []
counter = 0
counter_to_print = 0
path_count = 0
weight_count = 0
total_weight = 625 - 2
distance = []
current_algorithm = algorithms.Algorithm.BFS
euclidean = False
animation = True
visualise = False
DFS_bool = False
weights_on = False

running = True
mouse_down = False
right_mouse_down = False
#104, 157, 106
while running:
    screen.fill(colour) #(140,148,92) <- previous sidebar colour
    #pygame.draw.rect(screen,(104, 157, 106),(1055,30,350,900)) # sidebar

    #region - Drawing stuff
    box_colour = (201, 188, 153)
    weight_colour = (158, 147, 117)
    outline_colour = (50, 48, 47)
    wall_colour = (28, 27, 27)
    smaller_line = (69, 69, 69)
    start_colour = (93, 145, 71)
    goal_colour = (135, 54, 50)
    searched_colour = (131, 165, 152)#(69, 133, 136)
    frontier_colour = (8, 31, 56)
    node_colour = (87, 222, 84)
    path_colour = (250, 189, 47)
    offset_scl = 50



    sidebar_font = pygame.font.SysFont("lato", 80)
    algo_text_font = pygame.font.SysFont("lato", 40)
    normal_text_font = pygame.font.SysFont("lato", 25)
    header_font = pygame.font.SysFont("Consolas", 20)

    sidebar = pygame.Surface((350,900))
    sidebar.fill((104, 157, 106))

    title_text = sidebar_font.render(f"Grid Search", True, wall_colour)
    pygame.draw.line(sidebar, wall_colour, (17,70), (330,70), 1)
    algo_text = algo_text_font.render(f"{algorithms.algoNames[current_algorithm]}", True, outline_colour)
    sidebar.blit(title_text,(17,20))
    sidebar.blit(algo_text,(22,75))


    offset_legend = 110 
    tot_legend_off = 20

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 349 + offset_legend + offset_scl + tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,start_colour, (22, 350+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 369+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,goal_colour, (22, 370+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 389+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,wall_colour, (22, 390+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 409+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,searched_colour, (22, 410+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 429+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,frontier_colour, (22, 430+ offset_legend+ offset_scl+ tot_legend_off, 12, 12)) 

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 449+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,node_colour, (22, 450+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))


    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 469+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_weight_font = pygame.font.SysFont("lato",22)
    control_font = pygame.font.SysFont("lato",22)
    legend_weight_text = legend_weight_font.render("x", True,outline_colour)
    legend_start = pygame.draw.rect(sidebar,weight_colour, (22, 470+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))
    sidebar.blit(legend_weight_text, (24, 468+ offset_legend+ offset_scl+ tot_legend_off))

    legend_border = pygame.draw.rect(sidebar,outline_colour, (21, 489+ offset_legend+ offset_scl+ tot_legend_off, 14, 14))
    legend_start = pygame.draw.rect(sidebar,path_colour, (22, 490+ offset_legend+ offset_scl+ tot_legend_off, 12, 12))

    legend_header = header_font.render("Legend", True, wall_colour)
    pygame.draw.line(sidebar, wall_colour, (15,340+ + offset_legend+ offset_scl+ tot_legend_off), 
                     (330,340 + offset_legend+ offset_scl+ tot_legend_off), 1)

    legend_start_text = normal_text_font.render("Start cell", True, outline_colour)
    legend_goal_text = normal_text_font.render("Goal cell", True, outline_colour)
    legend_wall_text = normal_text_font.render("Wall", True, outline_colour)
    legend_searched_text = normal_text_font.render("Searched cell", True, outline_colour)
    legend_frontier_text = normal_text_font.render("Frontier cell", True, outline_colour)
    legend_node_text = normal_text_font.render("Node", True, outline_colour)
    legend_weighted_text = normal_text_font.render("Weighted cell", True, outline_colour)
    legend_shortestpath_text = normal_text_font.render("Path", True, outline_colour)

    sidebar.blit(legend_header,(15,320+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_start_text,(40,348+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_goal_text,(40,368+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_wall_text,(40,388+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_searched_text,(40,408+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_frontier_text,(40,428+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_node_text,(40,448+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_weighted_text,(40,468+ offset_legend+ offset_scl+ tot_legend_off))
    sidebar.blit(legend_shortestpath_text,(40,488+ offset_legend+ offset_scl+ tot_legend_off))
    control_off_tot = 53
    control_header = header_font.render("Controls", True, wall_colour)
    pygame.draw.line(sidebar, wall_colour, (15,647+ offset_scl+ control_off_tot), 
                     (330,647+ offset_scl+ control_off_tot), 1)


    controls_text1 = control_font.render("1-2-3-4-5 for BFS/DFS/DIJKSTRA/A*/GREEDY",True,outline_colour)
    controls_text5 = control_font.render("C - clears everything except walls/weights",True,outline_colour)
    controls_text3 = control_font.render("MOUSE1 - walls, MOUSE2 - wall removal",True,outline_colour)
    controls_text4 = control_font.render("W - weights, R - resets everything",True,outline_colour)
    controls_text2 = control_font.render("SPACE - start search, E - distance metric",True,outline_colour)
    offset_controls = 5
    sidebar.blit(control_header,(15,629+ offset_scl+ control_off_tot))
    sidebar.blit(controls_text1,(15,650+ offset_controls+ offset_scl + control_off_tot))
    sidebar.blit(controls_text2,(15,670+ offset_controls+ offset_scl+ control_off_tot))
    sidebar.blit(controls_text3,(15,690+ offset_controls+ offset_scl+ control_off_tot))
    sidebar.blit(controls_text4,(15,710+ offset_controls+ offset_scl+ control_off_tot))
    sidebar.blit(controls_text5,(15,730+ offset_controls+ offset_scl+ control_off_tot))

    
    # displaying algo descriptions
    if current_algorithm == algorithms.Algorithm.BFS:
        current_algo_desc = algorithms.bfs_desc
        time_complex_text = normal_text_font.render(f"Time:               O(V + E)", True, outline_colour)
        space_complex_text = normal_text_font.render(f"Space:             O(V)", True, outline_colour)
        frontier_algo_text = normal_text_font.render(f"Frontier:         FIFO queue", True, outline_colour)
        optimal_text = normal_text_font.render(f"Optimal:         Creates shortest path", True, outline_colour)

    if current_algorithm == algorithms.Algorithm.DFS:
        current_algo_desc = algorithms.dfs_desc
        time_complex_text = normal_text_font.render(f"Time:               O(V + E)", True, outline_colour)
        space_complex_text = normal_text_font.render(f"Space:             O(V)", True, outline_colour)
        frontier_algo_text = normal_text_font.render(f"Frontier:         LIFO stack", True, outline_colour)
        optimal_text = normal_text_font.render(f"Optimal:         Not guaranteed", True, outline_colour)

    if current_algorithm == algorithms.Algorithm.DIJSTRA:
        current_algo_desc = algorithms.dijkstra_desc
        time_complex_text = normal_text_font.render(f"Time:               O((V + E)log(V))", True, outline_colour)
        space_complex_text = normal_text_font.render(f"Space:             O(V)", True, outline_colour)
        frontier_algo_text = normal_text_font.render(f"Frontier:         min-prio queue", True, outline_colour)
        optimal_text = normal_text_font.render(f"Optimal:         Creates shortest path", True, outline_colour)

    if current_algorithm == algorithms.Algorithm.ASTAR:
        current_algo_desc = algorithms.astar_desc
        time_complex_text = normal_text_font.render(f"Time:               O(b^d) - worst case", True, outline_colour)
        space_complex_text = normal_text_font.render(f"Space:             O(b^d)", True, outline_colour)
        frontier_algo_text = normal_text_font.render(f"Frontier:         min-prio queue", True, outline_colour)
        optimal_text = normal_text_font.render(f"Optimal:         Creates shortest path", True, outline_colour)
    if current_algorithm == algorithms.Algorithm.GREEDY:
        current_algo_desc = algorithms.greedy_desc
        time_complex_text = normal_text_font.render(f"Time:               O(b^m) - worst case", True, outline_colour)
        space_complex_text = normal_text_font.render(f"Space:              O(b^m)", True, outline_colour)
        frontier_algo_text = normal_text_font.render(f"Frontier:         min-prio queue", True, outline_colour)
        optimal_text = normal_text_font.render(f"Optimal:            Not guaranteed", True, outline_colour)

    offset_desc = 0
    offset_4met = 15
    pygame.draw.line(sidebar, smaller_line, (20,248+ offset_4met), (325 ,248 + offset_4met), 1)
    for text in current_algo_desc:

        algo_desc_i = control_font.render(f"{text}", True, outline_colour)
        sidebar.blit(algo_desc_i,(20,254 + offset_desc+ offset_4met))
        offset_desc += 15

    sidebar.blit(time_complex_text,(20,110))
    sidebar.blit(space_complex_text,(20,130))
    sidebar.blit(frontier_algo_text,(20,150))
    sidebar.blit(optimal_text,(20,170))

    o_notation_desc_1 = control_font.render("V = # vertices, E = # edges, m = max depth",True,outline_colour)
    o_notation_desc_2 = control_font.render("d = depth of shallowest solution",True,outline_colour)
    o_notation_desc_3 = control_font.render("b = branching factor",True,outline_colour)
    pygame.draw.line(sidebar, smaller_line, (20,192+ offset_4met), (325 ,192+ offset_4met), 1)
    sidebar.blit(o_notation_desc_1,(20,200+ offset_4met))
    sidebar.blit(o_notation_desc_2,(20,215+ offset_4met))
    sidebar.blit(o_notation_desc_3,(20,230+ offset_4met))    
    





    #endregion - Drawing stuff

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                mouse_down = True
            if event.button == 3: # right click
                right_mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False

            if event.button == 3: 
                right_mouse_down = False

        if mouse_down or right_mouse_down:
            pix_x,pix_y = pygame.mouse.get_pos()
            position = pix2ord(pix_x,pix_y)

            if position is not None:
                row, col = position
                if (row, col) != (1, 1) and (row, col) != (23, 23):
                    if mouse_down:
                        classic.cells[row][col].wall = True
                    if right_mouse_down:
                        classic.cells[row][col].wall = False

        if event.type == pygame.KEYDOWN:        
            if event.key == pygame.K_r:    # r key
                classic.gridReset()
                path = []
                visualise = False
                counter_to_print = 0
                path_count = 0
                weights_on = False
                weight_count, total_weight = 0,623

            if event.key == pygame.K_e:       # e key
                euclidean = not euclidean
            
            if event.key == pygame.K_c:       # c key
                classic.gridClear()
                path = []
                visualise = False
                counter_to_print = 0
                path_count = 0

            if event.key == pygame.K_w:       # w key
                #classic.gridClear()
                path = []
                weights_on = True
                #visualise = False

                classic.giveWeights()
                weight_count, total_weight = classic.weightCount()


            if event.key == pygame.K_m:         # m key
                classic.gridReset()
                path = []
                counter_to_print = 0
                path_count = 0
                visualise = False
                weights_on = False
                weight_count, total_weight = 0,623

                algorithms.mazeGeneration(classic,euclidean)


            if event.key == pygame.K_1:          # 1
                current_algorithm = algorithms.Algorithm.BFS
                DFS_bool = False
                weights_on = False
                classic.gridClear()
                counter_to_print = 0
                path_count = 0
                path = []
                visualise = False
            if event.key == pygame.K_2:         # 2
                current_algorithm = algorithms.Algorithm.DFS
                DFS_bool = True
                weights_on = False
                counter_to_print = 0
                path_count = 0
                classic.gridClear()
                path = []
                visualise = False
            if event.key == pygame.K_3:          # 3
                current_algorithm = algorithms.Algorithm.DIJSTRA
                classic.gridClear()
                path = []
                path_count = 0
                weights_on = True
                visualise = False


            if event.key == pygame.K_SPACE:  # space
                classic.gridClear()
                path = []
                counter_to_print = 0
                path_count = 0
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
                        counter_to_print += 5 # since its in range(5) just add it at the end
                        break
                    
                    node.node = False # for drawing
                    queue, node, neighbours, visited,counter = result
                    counter_to_print += counter
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

                

                    



    #region text displaying live stats and such
    header_offset = 110
    stat_closer = - 10
    stat_header = header_font.render("Stats", True, wall_colour)
    pygame.draw.line(sidebar, wall_colour, (15,204+ header_offset+ offset_scl+ stat_closer), 
                     (330,204 + header_offset+ offset_scl+ stat_closer), 1)


    count_text = normal_text_font.render(f"Searched {counter_to_print}", True, (50, 48, 47))
    path_count_text = normal_text_font.render(f"Path amount {path_count}", True, (50, 48, 47))
    weight_count_text = normal_text_font.render(f"Amount of weights {weight_count}", True, (50, 48, 47))
    tot_weight_count_text = normal_text_font.render(f"Total weight {total_weight}", True, (50, 48, 47))
    
    euclidean_text = normal_text_font.render("Distance metric: Euclidean", True, (50, 48, 47))
    manhattan_text = normal_text_font.render("Distance metric: Manhattan", True, (50, 48, 47))

    sidebar.blit(stat_header, (15,184+ header_offset+ offset_scl + stat_closer))
    sidebar.blit(count_text, (15,270+ header_offset+ offset_scl+ stat_closer))
    sidebar.blit(path_count_text, (15,290+ header_offset+ offset_scl+ stat_closer))
    sidebar.blit(weight_count_text, (15,230+ header_offset+ offset_scl+ stat_closer))
    sidebar.blit(tot_weight_count_text, (15,250+ header_offset+ offset_scl+ stat_closer))

    if euclidean:
        sidebar.blit(euclidean_text, (15,210+ header_offset+ offset_scl+ stat_closer))
    else:
        sidebar.blit(manhattan_text, (15,210+ header_offset+ offset_scl+ stat_closer))

    #endregion 


    screen.blit(sidebar,(1055,30))
    pygame.draw.rect(screen, (66, 123, 88), (1055, 30, 350, 900), 8) # border
    drawGrid(grid_size_x,grid_size_y,classic)




    if path: # if path is non empty array
        #classic.gridReset()
        if weights_on:
            drawPath(classic,path)
            path_count = pathCount(path)
        else:
            path_count = drawPath(classic,path)


    # draw grid here

    pygame.display.flip()

pygame.quit()

