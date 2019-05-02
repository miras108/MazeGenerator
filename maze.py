import pygame
import inputbox
import time
import random
import slider
import sys

# sys.setrecursionlimit(20000)


class Point:
    MAX_VALUE = 30

    def __init__(self, x: int, y: int):
        if (x < 0 or y < 0) or (x > Point.MAX_VALUE or y > Point.MAX_VALUE):
            pass
        else:
            self._x = x
            self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class Maze:
    CORRIDOR = True

    def __init__(self, n_dim, m_dim, start_point: Point, end_point: Point):
        self.labirynth = [[False for j in range(n_dim)] for i in range(m_dim)]

        #TODO sprawdzenie start i end point
        self._width = n_dim
        self._height = m_dim
        self._start_point = start_point
        self._end_point = end_point
        self.labirynth[start_point.get_x()][start_point.get_y()] = Maze.CORRIDOR
        self.labirynth[end_point.get_x()][end_point.get_y()] = Maze.CORRIDOR

    def find_neighbours(self, point: Point):
        neighbours_list = []
        x, y = point.get_x(), point.get_y()
        if y - 1 >= 0:
            neighbours_list.append(Point(x, y-1))
        if y + 1 < self._height:
            neighbours_list.append(Point(x, y+1))
        if x - 1 >= 0:
            neighbours_list.append(Point(x-1,y))
        if x + 1 < self._width:
            neighbours_list.append(Point(x+1,y))

        return neighbours_list

    def find_neigbours_walls(self, point: Point):
        neighbours = self.find_neighbours(point)
        neighbours_walls_list = []
        for neighbour in neighbours:
            if self.labirynth[neighbour.get_x()][neighbour.get_y()] == False:
                neighbours_walls_list.append(neighbour)
        return neighbours_walls_list

    def find_neigbours_corridors(self, point: Point):
        neighbours = self.find_neighbours(point)
        neighbours_corridors_list = []
        for neighbour in neighbours:
            if self.labirynth[neighbour.get_x()][neighbour.get_y()] == True:
                neighbours_corridors_list.append(neighbour)
        return neighbours_corridors_list

    def get_first_neighbour_for_main_path(self):
        if self._start_point.get_x() == self._end_point.get_x():
            if self._start_point.get_x() == (n_dim - 1):
                return Point(self._start_point.get_x() - 1, self._start_point.get_y())
            else:
                return Point(self._start_point.get_x() + 1, self._start_point.get_y())

        elif self._start_point.get_y() == self._end_point.get_y():
            if self._start_point.get_y() == (m_dim - 1):
                return Point(self._start_point.get_x(), self._start_point.get_y() - 1)
            else:
                return Point(self._start_point.get_x(), self._start_point.get_y() + 1)
        else:
            neighbours = self.find_neigbours_walls(self._start_point)
            return random.choice(neighbours)

    def create_main_path(self):
        choosen_point = self._start_point
        # choosen_point = self.get_first_neighbour_for_main_path()
        # self.solution_stack = [choosen_point]
        self.solution_stack = []

        # self.labirynth[choosen_point.get_x()][choosen_point.get_y()] = True

        while True:
            neighbours = self.find_neigbours_walls(choosen_point)
            size = len(neighbours)
            for i in range(size):
                if(choosen_point is self._start_point):
                    choosen_point = self.get_first_neighbour_for_main_path()
                else:
                    choosen_point = random.choice(neighbours)
                neighbours_corridors = self.find_neigbours_corridors(choosen_point)

                if len(neighbours_corridors) == 1:
                    self.labirynth[choosen_point.get_x()][choosen_point.get_y()] = True
                    self.solution_stack.append(choosen_point)
                    break
                else:
                    if len(neighbours_corridors) == 2 and ((neighbours_corridors[0].get_x() == self._end_point.get_x() and neighbours_corridors[0].get_y() == self._end_point.get_y()) or (neighbours_corridors[1].get_x() == self._end_point.get_x() and neighbours_corridors[1].get_y() == self._end_point.get_y())):
                        self.labirynth[choosen_point.get_x()][choosen_point.get_y()] = True
                        self.solution_stack.append(choosen_point)
                        return None
                    else:
                        neighbours.remove(choosen_point)

            else:
                self.solution_stack.pop()
                if len(self.solution_stack) != 0:
                    choosen_point = self.solution_stack[len(self.solution_stack) - 1]
                else:
                    choosen_point = self._start_point

    def create_additional_path(self, start_point: Point):
        choosen_point = start_point
        additional_path = [start_point]

        while True:
            neighbours = self.find_neigbours_walls(choosen_point)
            size = len(neighbours)
            for i in range(size):
                choosen_point = random.choice(neighbours)
                neighbours_corridors = self.find_neigbours_corridors(choosen_point)

                if len(neighbours_corridors) == 1:
                    self.labirynth[choosen_point.get_x()][choosen_point.get_y()] = True
                    additional_path.append(choosen_point)
                    break
                else:
                    neighbours.remove(choosen_point)

            else:
                if len(additional_path) > 1:
                    additional_path.pop()
                    choosen_point = additional_path[len(additional_path) - 1]
                else:
                    return None

    def create_additionals_path(self):
        for stack_point in self.solution_stack:
            self.create_additional_path(stack_point)

    def tmp_read_input(self):
        x = int(input('x = '))
        y = int(input('y = '))
        return Point(x, y)

    def append_path(self, path, point: Point, previous_neighbour: Point):
        print(point.get_x(), point.get_y())
        for c in self.solution_stack:
            if point.get_x() == c.get_x() and point.get_y() == c.get_y():
                return path

        for c in path:
            if point.get_x() == c.get_x() and point.get_y() == c.get_y():
                return None

        neighbours_corridors = self.find_neigbours_corridors(point)
        for corridor in neighbours_corridors:
            if previous_neighbour is None or not (previous_neighbour.get_x() == corridor.get_x() and previous_neighbour.get_y() == corridor.get_y()):
                x = self.append_path(path, corridor, point)
                if x is not None:
                    x.append(point)
                    return x

        else:
            return None

    def add_inter_point(self):
        point = self.tmp_read_input()
        path = []
        path = self.append_path(path, point, None)
        self.solution_stack += path
        #
        # previous_corridor = point
        # while True:
        #     neighbour_corridor = self.find_neigbours_corridors(point)
        #     #neighbour_corridor.remove(previous_corridor)
        #     for corridor in range(len(neighbour_corridor)):
        #         if corridor in self.solution_stack:
        #             self.solution_stack += path
        #             return None
        #         else:
        #             previous_corridor = corridor
        #             next_corridor = random.choice(neighbour_corridor)
        #             break


    def tmp_print_maze(self):
        print()
        for i in range(self._height):
            for j in range(self._width):
                if self.labirynth[i][j]:
                    print(1, end='\t')
                else:
                    print(0, end='\t')
            print()

    def tmp_print_solution(self):
        print()
        path = self.solution_stack.pop()
        while path:
            print(path.get_x(), path.get_y())
            path = self.solution_stack.pop()


n_dim = int(inputbox.display_input_box(400, 400, 'WIDTH'))
m_dim = int(inputbox.display_input_box(400, 400, 'HEIGHT'))
m = Maze(n_dim, m_dim, Point(0, 0), Point(15, 15))
m.create_main_path()
m.create_additionals_path()


# m.tmp_print_maze()
#m.create_additional_path()
# m.tmp_print_maze()
#m.tmp_print_solution()

# set up pygame window
WIDTH = 1280
HEIGHT = 1024
FPS = 30

# Define colours
WHITE = (255, 255, 255)
BRIGHT_GREEN = (0, 255, 125)
GREEN = (0, 255, 40)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
RED = (200, 0, 0)
BRIGHT_RED = (200, 0, 100)
BLACK = (0, 0, 0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 30                   # width of cell
grid_start_point = Point(20, 20)

def build_grid(maze: Maze):
    y = grid_start_point.get_y()                                                        # start a new row
    for i in range(maze._height):
        x = grid_start_point.get_x()                                                            # set x coordinate to start position
        for j in range(maze._width):
            if maze.labirynth[i][j] == True:
                p = Point(i, j)
                if (p.get_x() == maze._start_point.get_x() and p.get_y() == maze._start_point.get_y()) or \
                        (p.get_x() == maze._end_point.get_x() and p.get_y() == maze._end_point.get_y()):
                    pygame.draw.rect(screen, RED, (x, y, w - 2, w - 2))
                else:
                    for sol in maze.solution_stack:
                        if sol.get_x() == p.get_x() and sol.get_y() == p.get_y():
                            pygame.draw.rect(screen, GREEN, (x, y, w - 2, w - 2))
                            break
                    else:
                        pygame.draw.rect(screen, BLUE, (x, y, w - 2, w - 2))
            else:
                pygame.draw.rect(screen, WHITE, (x, y, w-2, w-2))

            #grid.append((x, y))                                           # add cell to grid list
            x = x + w                                                    # move cell to new position
        y = y + w
build_grid(m)
pygame.display.update()

m.add_inter_point()
build_grid(m)
pygame.display.update()


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def add_button(x, y, dx, dy, message, inactive_colour, active_colour, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    small_text = pygame.font.Font('freesansbold.ttf', 20)

    # GENERATE BUTTON
    if x < mouse[0] < x + dx and y < mouse[1] < y + dy:
        pygame.draw.rect(screen, active_colour, (x, y, dx, dy), 0)
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, dx, dy), 0)

    text_surface, text_rectangle = text_objects(message, small_text)
    text_rectangle.center = ((x + dx/2), (y + dy/2))
    screen.blit(text_surface, text_rectangle)

def add_square(point: Point, width, inactive_colour, active_colour, action, starting_position):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    start_pos = starting_position
    #small_text = pygame.font.Font('freesansbold.ttf', 20)
    dx = (point.get_x()) * width + start_pos
    dy = (point.get_x()) * width + start_pos

    # GENERATE BUTTON
    if dx < mouse[0] < dx + width and dy < mouse[1] < dy + width:
        pygame.draw.rect(screen, active_colour, (dx, dy, dx+width, dy+width), 0)
        # if click[0] == 1:
        #     action()
    else:
        pygame.draw.rect(screen, inactive_colour, (dx, dy, dx+width, dy+width), 0)

def build_grid(maze: Maze):
    starting_position = 20
    #y = grid_start_point.get_y()                                                        # start a new row
    for i in range(maze._height):
        #x = grid_start_point.get_x()                                                            # set x coordinate to start position
        for j in range(maze._width):
            if maze.labirynth[i][j] == True:
                p = Point(i, j)
                if (p.get_x() == maze._start_point.get_x() and p.get_y() == maze._start_point.get_y()) or \
                        (p.get_x() == maze._end_point.get_x() and p.get_y() == maze._end_point.get_y()):
                    add_square(p, w, RED, YELLOW)
                else:
                    for sol in maze.solution_stack:
                        if sol.get_x() == p.get_x() and sol.get_y() == p.get_y():
                            pygame.draw.rect(screen, GREEN, (x, y, w - 2, w - 2))
                            break
                    else:
                        pygame.draw.rect(screen, BLUE, (x, y, w - 2, w - 2))
            else:
                pygame.draw.rect(screen, WHITE, (x, y, w-2, w-2))

            #grid.append((x, y))                                           # add cell to grid list
            x = x + w                                                    # move cell to new position
        y = y + w


##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    pygame.display.update()
    add_button(1100, 800, 150, 50, 'Quit...', RED, BRIGHT_RED, quit)


    # process input (events)
    for event in pygame.event.get():

        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN and event.key ==




def generate():
    x, y = 20, 20  # starting position of grid
    build_grid(40, 0, 20)  # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
    # carve_out_maze(x, y)  # call build the maze function
    # plot_route_back(400, 400)  # call the plot solution function
    # plot_route_back(400, 20)  # call the plot solution function
    # plot_route_back(20, 400)  # call the plot solution function
    # plot_route_back(400, 300)  # call the plot solution function

# #####################################################################################################################
# # set up pygame window
# WIDTH = 800
# HEIGHT = 600
# FPS = 30
#
# # Define colours
# WHITE = (255, 255, 255)
# BRIGHT_GREEN = (0, 255, 125)
# GREEN = (0, 255, 40)
# BLUE = (0, 0, 255)
# YELLOW = (255 ,255 ,0)
# RED = (200, 0, 0)
# BRIGHT_RED = (200, 0, 100)
# BLACK = (0, 0, 0)
#
# # initalise Pygame
# pygame.init()
# pygame.mixer.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Maze Generator")
# clock = pygame.time.Clock()
#
# # setup maze variables
# x = 0                    # x axis
# y = 0                    # y axis
# w = 20                   # width of cell
# grid = []
# visited = []
# stack = []
# solution = {}
#
#
# # build the grid
# def build_grid(x, y, w):
#     for i in range(1,21):
#         x = 20                                                            # set x coordinate to start position
#         y = y + 20                                                        # start a new row
#         for j in range(1, 21):
#             pygame.draw.rect(screen, WHITE, (x, y, w, w))
#             pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
#             pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
#             pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
#             pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell
#             grid.append((x, y))                                           # add cell to grid list
#             x = x + 20                                                    # move cell to new position
#
#
# def push_up(x, y):
#     pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # draw a rectangle twice the width of the cell
#     pygame.display.update()                                              # to animate the wall being removed
#
#
# def push_down(x, y):
#     pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 39), 0)
#     pygame.display.update()
#
#
# def push_left(x, y):
#     pygame.draw.rect(screen, BLUE, (x - w + 1, y + 1, 39, 19), 0)
#     pygame.display.update()
#
#
# def push_right(x, y):
#     pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 39, 19), 0)
#     pygame.display.update()
#
#
# def single_cell( x, y):
#     pygame.draw.rect(screen, GREEN, (x +1, y +1, 18, 18), 0)          # draw a single width cell
#     pygame.display.update()
#
#
# def backtracking_cell(x, y):
#     pygame.draw.rect(screen, BLUE, (x +1, y +1, 18, 18), 0)        # used to re-colour the path after single_cell
#     pygame.display.update()                                        # has visited cell
#
#
# def solution_cell(x,y):
#     pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
#     pygame.display.update()                                        # has visited cell
#
#
# def carve_out_maze(x,y):
#     single_cell(x, y)                                              # starting positing of maze
#     stack.append((x,y))                                            # place starting cell into stack
#     visited.append((x,y))                                          # add starting cell to visited list
#     while len(stack) > 0:                                          # loop until stack is empty
#         #time.sleep(.07)                                            # slow program now a bit
#         #add_button(600, 440, 150, 50, 'Generate', GREEN, BRIGHT_GREEN)
#         #add_button(600, 500, 150, 50, 'Quit...', RED, BRIGHT_RED, pygame.quit())
#
#         cell = []                                                  # define cell list
#         if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
#             cell.append("right")                                   # if yes add to cell list
#
#         if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
#             cell.append("left")
#
#         if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
#             cell.append("down")
#
#         if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
#             cell.append("up")
#
#         if len(cell) > 0:                                          # check to see if cell list is empty
#             cell_chosen = (random.choice(cell))                    # select one of the cell randomly
#
#             if cell_chosen == "right":                             # if this cell has been chosen
#                 push_right(x, y)                                   # call push_right function
#                 solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
#                 x = x + w                                          # make this cell the current cell
#                 visited.append((x, y))                              # add to visited list
#                 stack.append((x, y))                                # place current cell on to stack
#
#             elif cell_chosen == "left":
#                 push_left(x, y)
#                 solution[(x - w, y)] = x, y
#                 x = x - w
#                 visited.append((x, y))
#                 stack.append((x, y))
#
#             elif cell_chosen == "down":
#                 push_down(x, y)
#                 solution[(x , y + w)] = x, y
#                 y = y + w
#                 visited.append((x, y))
#                 stack.append((x, y))
#
#             elif cell_chosen == "up":
#                 push_up(x, y)
#                 solution[(x , y - w)] = x, y
#                 y = y - w
#                 visited.append((x, y))
#                 stack.append((x, y))
#         else:
#             x, y = stack.pop()                                    # if no cells are available pop one from the stack
#             single_cell(x, y)                                     # use single_cell function to show backtracking image
#             time.sleep(.05)                                       # slow program down a bit
#             backtracking_cell(x, y)                               # change colour to green to identify backtracking path
#
#
# def plot_route_back(x,y):
#     solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
#     while (x, y) != (20,20):                                     # loop until cell position == start position
#         x, y = solution[x, y]                                    # "key value" now becomes the new key
#         solution_cell(x, y)                                      # animate route back
#         time.sleep(.1)
#
#
# # MY FUNCTIONS
#
def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def add_button(x, y, dx, dy, message, inactive_colour, active_colour, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    small_text = pygame.font.Font('freesansbold.ttf', 20)

    # GENERATE BUTTON
    if x < mouse[0] < x + dx and y < mouse[1] < y + dy:
        pygame.draw.rect(screen, active_colour, (x, y, dx, dy), 0)
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, dx, dy), 0)

    text_surface, text_rectangle = text_objects(message, small_text)
    text_rectangle.center = ((x + dx/2), (y + dy/2))
    screen.blit(text_surface, text_rectangle)
#
#
# def generate():
#     x, y = 20, 20  # starting position of grid
#     build_grid(40, 0, 20)  # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
#     carve_out_maze(x, y)  # call build the maze function
#     plot_route_back(400, 400)  # call the plot solution function
#     plot_route_back(400, 20)  # call the plot solution function
#     plot_route_back(20, 400)  # call the plot solution function
#     #plot_route_back(400, 300)  # call the plot solution function
#
#
# def quit_application():
#     pygame.quit()
#     quit()
#
# # ##### pygame loop #######
# running = True
# while running:
#     # keep running at the at the right speed
#     clock.tick(FPS)
#     add_button(600, 440, 150, 50, 'Generate', GREEN, BRIGHT_GREEN, generate)
#     add_button(600, 500, 150, 50, 'Quit...', RED, BRIGHT_RED, quit_application)
#     pygame.display.update()
#
#     # process input (events)
#     for event in pygame.event.get():
#
#         # check for closing the window
#         if event.type == pygame.QUIT:
#             running = False
