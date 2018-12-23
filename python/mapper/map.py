import numpy as np
from utils.position import Position

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
