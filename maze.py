import pygame
import inputbox
import time
import random
from maze_exceptions import *

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

    def __eq__(self, other):
        if self.get_x() == other.get_x() and self.get_y() == other.get_y():
            return True
        else:
            return False

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class Maze:
    CORRIDOR = True

    def __init__(self, n_dim, m_dim, start_point: Point, end_point: Point):
        self.labirynth = [[False for j in range(m_dim)] for i in range(n_dim)]



        self._width = m_dim
        self._height = n_dim
        self._start_point = start_point
        self._end_point = end_point
        self.labirynth[start_point.get_x()][start_point.get_y()] = Maze.CORRIDOR
        self.labirynth[end_point.get_x()][end_point.get_y()] = Maze.CORRIDOR
        self.inter_points = []
        #self.main_path = []
        #TODO sprawdzenie start i end point i sasiedztwa
        neighbour_of_start_point = self.find_neighbours(start_point)
        if start_point == end_point or end_point in neighbour_of_start_point:
            raise WrongStartingPointException

    def find_neighbours(self, point: Point):
        neighbours_list = []
        x, y = point.get_x(), point.get_y()
        if y - 1 >= 0:
            neighbours_list.append(Point(x, y-1))
        if y + 1 < self._width:
            neighbours_list.append(Point(x, y+1))
        if x - 1 >= 0:
            neighbours_list.append(Point(x-1,y))
        if x + 1 < self._height:
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
                        self.main_path = [field for field in self.solution_stack]
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

    # def add_inter_point(self):
    #     point = self.tmp_read_input()
    #     path = []
    #     # Sprawdzanie czy point jest corridorem
    #     self.inter_points.append(point)
    #     path = self.append_path(path, point, None)
    #     self.solution_stack += path

    def add_inter_point(self, point: Point):
        path = []
        # Sprawdzanie czy point jest corridorem
        self.inter_points.append(point)
        path = self.append_path(path, point, None)
        self.solution_stack += path

    def add_inter_point_tmp(self, point: Point):
        #point = self.tmp_read_input()
        path = []
        # Sprawdzanie czy point jest corridorem
        #self.inter_points.append(point)
        path = self.append_path(path, point, None)
        self.solution_stack += path

    def remove_path(self, path, point: Point, previous_neighbour: Point):
        print(point.get_x(), point.get_y())
        for c in self.main_path:
            if point.get_x() == c.get_x() and point.get_y() == c.get_y():
                return path

        for c in path:
            if point.get_x() == c.get_x() and point.get_y() == c.get_y():
                return None

        neighbours_corridors = self.find_neigbours_corridors(point)
        for corridor in neighbours_corridors:
            if previous_neighbour is None or not (previous_neighbour.get_x() == corridor.get_x() and previous_neighbour.get_y() == corridor.get_y()):
                x = self.remove_path(path, corridor, point)
                if x is not None:
                    x.append(point)
                    return x

        else:
            return None

    # def remove_inter_point(self):
    #     path = []
    #     point = self.tmp_read_input()
    #     # Sprawdzanie czy point jest corridorem i czy jest w inter_points
    #     for inter_point in self.inter_points:
    #         if inter_point.get_x() == point.get_x() and inter_point.get_y() == point.get_y():
    #             self.inter_points.remove(inter_point)
    #     path = self.remove_path(path, point, None)
    #     self.solution_stack = [p for p in self.solution_stack if p not in path]
    #     for ip in self.inter_points:
    #         path = []
    #         path = self.remove_path(path, ip, None)
    #         self.solution_stack = [p for p in self.solution_stack if p not in path]
    #         self.add_inter_point_tmp(ip)

    def remove_inter_point(self, point):
        path = []
        # Sprawdzanie czy point jest corridorem i czy jest w inter_points
        for inter_point in self.inter_points:
            if inter_point.get_x() == point.get_x() and inter_point.get_y() == point.get_y():
                self.inter_points.remove(inter_point)
        path = self.remove_path(path, point, None)
        self.solution_stack = [p for p in self.solution_stack if p not in path]
        for ip in self.inter_points:
            path = []
            path = self.remove_path(path, ip, None)
            self.solution_stack = [p for p in self.solution_stack if p not in path]
            self.add_inter_point_tmp(ip)

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


# NEEDS CHECKING!
def check_if_valid_input_dim(dim: int):
    try:
        if dim < 2 or dim > 30:
            raise WrongInputException
        else:
            return dim

    except WrongInputException as err:
        dim = err.handling()
        #dim = int(inputbox.display_input_box(400,400,'SIZE'))
        return check_if_valid_input_dim(dim)

m_dim = int(inputbox.display_input_box(400, 400, 'WIDTH'))
m_dim = check_if_valid_input_dim(m_dim)
n_dim = int(inputbox.display_input_box(400, 400, 'HEIGHT'))
n_dim = check_if_valid_input_dim(n_dim)


# x_start = int(inputbox.display_input_box(400, 400, 'x_start'))
# y_start = int(inputbox.display_input_box(400, 400, 'y_start'))
# start = Point(x_start, y_start)
#
#
# x_end = int(inputbox.display_input_box(400, 400, 'x_end'))
# y_end = int(inputbox.display_input_box(400, 400, 'y_end'))
# end = Point(x_end, y_end)

# m = Maze(n_dim,m_dim,start,end)
# m.create_main_path()
# m.create_additionals_path()

#pygame.display.update()

# m = Maze(n_dim, m_dim, Point(0, 5), Point(0, 8))
# m.create_main_path()
# m.create_additionals_path()


# m.tmp_print_maze()
#m.create_additional_path()
# m.tmp_print_maze()
#m.tmp_print_solution()

# set up pygame window
WIDTH = 1280
HEIGHT = 1000
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
#build_grid(m)
#pygame.display.update()

# m.add_inter_point()
# build_grid(m)
# pygame.display.update()
# m.add_inter_point()
# build_grid(m)
# pygame.display.update()
# m.remove_inter_point()
# build_grid(m)
# pygame.display.update()

def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


end_and_start_points = []
def return_point_coords(point: Point):
    global end_and_start_points
    if len(end_and_start_points) != 2:
        end_and_start_points.append(point)

def generate_initial_maze(n_dim, m_dim):
    starting_position = 20
    for i in range(n_dim):
        for j in range(m_dim):
            p = Point(i, j)
            add_square(p, w, WHITE, YELLOW, action= return_point_coords)
    maze = Maze(n_dim, m_dim, end_and_start_points[0], end_and_start_points[1])
    maze.create_main_path()
    maze.create_additionals_path()
    return maze

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

def add_square(point: Point, width, inactive_colour, active_colour, action = None, starting_position = 20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    start_pos = starting_position
    dx = (point.get_y()) * width + start_pos
    dy = (point.get_x()) * width + start_pos

    # GENERATE BUTTON
    if dx < mouse[0] < dx + width and dy < mouse[1] < dy + width:
        pygame.draw.rect(screen, active_colour, (dx, dy, width - 2, width - 2), 0)
        if click[0] == 1:
            if action is not None:
                action(point)
                time.sleep(.25)
    else:
        pygame.draw.rect(screen, inactive_colour, (dx, dy, width - 2, width - 2), 0)

##### pygame loop #######
i = 0

m: Maze = None

m = None
generate_triggered = False

def generate():
    global generate_triggered
    global m
    if m is not None:
        for i in range(m._height):
            for j in range(m._width):
                p = Point(i,j)
                if m.labirynth[i][j] == True:
                    if (p.get_x() == m._start_point.get_x() and p.get_y() == m._start_point.get_y()) or \
                            (p.get_x() == m._end_point.get_x() and p.get_y() == m._end_point.get_y()):
                        add_square(p,w,RED,YELLOW)
                    elif p in m.inter_points:
                        add_square(p,w,BRIGHT_RED,YELLOW,action=m.remove_inter_point)
                    else:
                        for sol in m.solution_stack:
                            if sol.get_x() == p.get_x() and sol.get_y() == p.get_y():
                                add_square(p,w,GREEN,YELLOW)
                                break
                        else:
                            add_square(p,w,BLUE,YELLOW,action=m.add_inter_point)
                else:
                    add_square(p,w,WHITE,YELLOW)
    generate_triggered = True


running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    pygame.display.update()
    add_button(1100, 800, 150, 50, 'Quit...', RED, BRIGHT_RED, quit)
    if m is not None:
        add_button(1100, 600, 150, 50, 'Generate', GREEN, BRIGHT_GREEN, generate)


########################################################################################################
    if m is None:
        for i in range(n_dim):
            for j in range(m_dim):
                p = Point(i,j)
                if p in end_and_start_points:
                    add_square(p,w,BRIGHT_GREEN,YELLOW, action=return_point_coords)
                else:
                    add_square(p,w,WHITE,YELLOW, action=return_point_coords)



    if len(end_and_start_points) == 2:
        try:
            m = Maze(n_dim, m_dim, end_and_start_points[0], end_and_start_points[1])
            m.create_main_path()
            m.create_additionals_path()
        except WrongStartingPointException as err:
            m = None
            #err.handling()
        end_and_start_points.clear()


########################################################################################################


    if generate_triggered:
        starting_position = 20
        # y = grid_start_point.get_y()                                                        # start a new row
        for i in range(m._height):
            # x = grid_start_point.get_x()                                                            # set x coordinate to start position
            for j in range(m._width):
                p = Point(i,j)
                if m.labirynth[i][j] == True:
                    if (p.get_x() == m._start_point.get_x() and p.get_y() == m._start_point.get_y()) or \
                            (p.get_x() == m._end_point.get_x() and p.get_y() == m._end_point.get_y()):
                        add_square(p,w,RED,YELLOW)
                    elif p in m.inter_points:
                        add_square(p,w,BRIGHT_RED,YELLOW,action=m.remove_inter_point)
                    else:
                        for sol in m.solution_stack:
                            if sol.get_x() == p.get_x() and sol.get_y() == p.get_y():
                                add_square(p,w,GREEN,YELLOW)
                                # pygame.draw.rect(screen, GREEN, (x, y, w - 2, w - 2))
                                break
                        else:
                            add_square(p,w,BLUE,YELLOW,action=m.add_inter_point)
                            # pygame.draw.rect(screen, BLUE, (x, y, w - 2, w - 2))
                else:
                    add_square(p,w,WHITE,YELLOW)
            #         # pygame.draw.rect(screen, WHITE, (x, y, w-2, w-2))
            #
            #     # grid.append((x, y))                                           # add cell to grid list
            #     x = x + w  # move cell to new position
            # y = y + w

##########################################################################################

    # process input (events)
    for event in pygame.event.get():

        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
