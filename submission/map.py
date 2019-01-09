import numpy as np
from position import Position
from utils import von_neumann_neighbourhood, moore_neighbourhood

class Map:
    """
    Class that implements the Map object, used to contain the grid of the environment and useful functions.
    """

    def __init__(self, lower_left_pos, upper_right_pos, scale):
        """
        Instantiates a Map.
        :param lower_left_pos: The lower left point of the environment to explore.
        :type lower_left_pos: Position
        :param upper_right_pos: The upper right point of the environment to explore.
        :type upper_right_pos: Position
        :param scale: Scale to apply to convert real world positions to grid positions.
        :type scale: float
        """
        self.__lower_left_pos = lower_left_pos
        self.__upper_right_pos = upper_right_pos
        self.__scale = scale
        self.__real_width = upper_right_pos.x - lower_left_pos.x 
        self.__grid_width = int(self.__real_width * scale)
        self.__real_height = upper_right_pos.y - lower_left_pos.y 
        self.__grid_height = int(self.__real_height * scale)
        self.grid = np.full((self.__grid_width, self.__grid_height), 0.5)

    def to_grid_pos(self, real_pos):
        """
        Converts a real position into a grid position.
        :param real_pos: The real world position.
        :type real_pos: Position
        :return: The grid position.
        :rtype: Position
        """
        x = int((real_pos.x - self.__lower_left_pos.x) * self.__scale)
        y = int((real_pos.y - self.__lower_left_pos.y) * self.__scale)
        return Position(x, y)

    def to_real_pos(self, grid_pos):
        """
        Converts a grid position into a real position.
        :param grid_pos: The grid position.
        :type grid_pos: Position
        :return: The real world position.
        :rtype: Position
        """
        x = (grid_pos.x / self.__scale) + self.__lower_left_pos.x
        y = (grid_pos.y / self.__scale) + self.__lower_left_pos.y
        return Position(x, y)

    def is_in_bound(self, grid_pos):
        """
        Tells if the given cell is in bounds or not.
        :param grid_pos: The grid position.
        :type grid_pos: Position
        :return: True if the cell is in bounds, False otherwise.
        :rtype: boolean
        """
        return 0 <= grid_pos.x < self.__grid_width and 0 <= grid_pos.y < self.__grid_height

    def is_unknown(self, grid_pos):
        """
        Tells if the given cell is unknown or not.
        :param grid_pos: The grid position.
        :type grid_pos: Position
        :return: True if the cell is unknown, False otherwise.
        :rtype: boolean
        """
        return self.grid[grid_pos.x][grid_pos.y] == 0.5

    def is_obstacle(self, grid_pos):
        """
        Tells if the given cell is an obstacle or not.
        :param grid_pos: The grid position.
        :type grid_pos: Position
        :return: True if the cell is an obstacle, False otherwise.
        :rtype: boolean
        """
        return self.grid[grid_pos.x][grid_pos.y] > 0.5

    def is_empty(self, grid_pos):
        """
        Tells if the given cell is empty or not.
        :param grid_pos: The grid position.
        :type grid_pos: Position
        :return: True if the cell is empty, False otherwise.
        :rtype: boolean
        """
        return self.grid[grid_pos.x][grid_pos.y] < 0.5

    @property
    def grid_width(self):
        """
        Gives the grid width.
        :return: The width of the grid.
        :rtype: integer
        """
        return self.__grid_width

    @property
    def grid_height(self):
        """
        Gives the grid height.
        :return: The height of the grid.
        :rtype: integer
        """
        return self.__grid_height
