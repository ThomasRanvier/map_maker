import numpy as np
from utils.position import Position
from utils.utils import von_neumann_neighbourhood, moore_neighbourhood

class Map:
    def __init__(self, lower_left_pos, upper_right_pos, scale):
        self.__lower_left_pos = lower_left_pos
        self.__upper_right_pos = upper_right_pos
        self.__scale = scale
        self.__real_width = upper_right_pos.x - lower_left_pos.x 
        self.__grid_width = int(self.__real_width * scale)
        self.__real_height = upper_right_pos.y - lower_left_pos.y 
        self.__grid_height = int(self.__real_height * scale)
        self.grid = np.full((self.__grid_width, self.__grid_height), 0.5)

    def to_grid_pos(self, real_pos):
        x = int((real_pos.x - self.__lower_left_pos.x) * self.__scale)
        y = int((real_pos.y - self.__lower_left_pos.y) * self.__scale)
        return Position(x, y)

    def to_real_pos(self, grid_pos):
        x = (grid_pos.x / self.__scale) + self.__lower_left_pos.x
        y = (grid_pos.y / self.__scale) + self.__lower_left_pos.y
        return Position(x, y)

    def is_in_bound(self, grid_pos):
        return 0 <= grid_pos.x < self.__grid_width and 0 <= grid_pos.y < self.__grid_height

    def is_unknown(self, grid_pos):
        return self.grid[grid_pos.x][grid_pos.y] == 0.5

    def is_obstacle(self, grid_pos):
        return self.grid[grid_pos.x][grid_pos.y] > 0.5

    def is_empty(self, grid_pos):
        return self.grid[grid_pos.x][grid_pos.y] < 0.5

    @property
    def grid_width(self):
        return self.__grid_width

    @property
    def grid_height(self):
        return self.__grid_height

    def __get_frontiers(self):
        frontiers = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                cell = Position(x, y)
                if self.is_unknown(cell):
                    for neighbour in von_neumann_neighbourhood(cell, self.grid_width, self.grid_height):
                        if neighbour not in frontiers and self.grid[neighbour.x][neighbour.y] <= 0.1:#is_empty(neighbour):
                            frontiers.append(neighbour)
        return frontiers

    def __build_frontier(self, frontiers, current_frontier, cell):
        neighbours = moore_neighbourhood(cell, self.grid_width, self.grid_height)
        for neighbour in neighbours:
            if neighbour in frontiers:
                current_frontier.append(neighbour)
                frontiers.remove(neighbour)
                self.__build_frontier(frontiers, current_frontier, neighbour)

    def get_divided_frontiers(self):
        frontiers = self.__get_frontiers()
        divided_frontiers = []
        while frontiers:
            current_frontier = []
            cell = frontiers.pop(0)
            current_frontier.append(cell)
            self.__build_frontier(frontiers, current_frontier, cell)
            divided_frontiers.append(current_frontier)
        return divided_frontiers
