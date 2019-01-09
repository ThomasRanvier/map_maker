from utils import bresenham_line
from math import hypot, cos, sin
from position import Position

class Cartographer:
    """
    Class that implements a Cartographer, used to update the map of the environment using the lasers echoes.
    """
    
    def __init__(self, lasers_distance = 0.15, min_increment = 0.015, increment = 0.15, max_distance = 40, safe_distance_obstacle = 5, safe_distance_empty = 10):
        """
        Instantiates a Cartographer.
        :param lasers_distance: Offset of the lasers in regard of the robot.
        :type lasers_distance: float
        :param min_increment: Minimal increment for update of the cells of the map.
        :type min_increment: float
        :param increment: Increment for update of the cells of the map.
        :type increment: float
        :param max_distance: Maximum distance of the echoes.
        :type max_distance: float
        :param safe_distance_obstacle: Used to be more precise on echoes readings.
        :type safe_distance_obstacle: float
        :param safe_distance_obstacle: Used to be more precise on echoes readings.
        :type safe_distance_obstacle: float
        """
        self.__lasers_distance = lasers_distance
        self.__max_distance = max_distance
        self.__min_increment = min_increment
        self.__increment = increment
        self.__safe_distance_obstacle = safe_distance_obstacle
        self.__safe_distance_empty = safe_distance_empty
        
    def update(self, robot_map, robot_pos, lasers):
        """
        Function used to update the map by analyzing the lasers echoes, it uses the Bresenham line algorithm (implemented in utils.utils) to update lines.
        :param robot_map: The map to update.
        :type robot_map: Map
        :param robot_pos: Robot position in the real world.
        :type robot_pos: Position
        :param lasers: The lasers datas.
        :type lasers: A list of Laser objects.
        :return: The map updated.
        :rtype: Map
        """
        lasers_pos_x = robot_pos.x + self.__lasers_distance * cos(robot_pos.angle)
        lasers_pos_y = robot_pos.y + self.__lasers_distance * sin(robot_pos.angle)
        lasers_cell = robot_map.to_grid_pos(Position(lasers_pos_x, lasers_pos_y))
        real_lasers_cell = robot_map.to_real_pos(lasers_cell)
        for laser in lasers:
            angle = robot_pos.angle + laser.angle
            laser_hit = Position(lasers_pos_x + laser.echoe * cos(angle), lasers_pos_y + laser.echoe * sin(angle))
            hit_cell = robot_map.to_grid_pos(laser_hit)
            cells = bresenham_line(lasers_cell.x, lasers_cell.y, hit_cell.x, hit_cell.y)
            for cell in cells:
                if robot_map.is_in_bound(cell):
                    if cell.x == hit_cell.x and cell.y == hit_cell.y:
                        if laser.echoe < self.__max_distance - self.__safe_distance_obstacle:
                            inc_iro_certainty = self.__min_increment if robot_map.is_empty(cell) else self.__increment
                            inc_factor_iro_dist = (1.0 - (laser.echoe / self.__max_distance))
                            robot_map.grid[cell.x][cell.y] += inc_factor_iro_dist * inc_iro_certainty 
                            if robot_map.grid[cell.x][cell.y] > 1.0:
                                robot_map.grid[cell.x][cell.y] = 1.0
                    else:
                        real_cell = robot_map.to_real_pos(cell)
                        distance = hypot(real_cell.x - real_lasers_cell.x, real_cell.y - real_lasers_cell.y)
                        if distance < self.__max_distance - self.__safe_distance_empty:
                            inc_iro_certainty = self.__min_increment if robot_map.is_obstacle(cell) else self.__increment
                            inc_factor_iro_dist = (1.0 - (distance / self.__max_distance))
                            robot_map.grid[cell.x][cell.y] -= inc_factor_iro_dist * inc_iro_certainty
                            if robot_map.grid[cell.x][cell.y] < 0.0:
                                robot_map.grid[cell.x][cell.y] = 0.0
        return robot_map
