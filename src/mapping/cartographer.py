from utils.utils import bresenham_line
from math import hypot, cos, sin, pi
from mapping.map import Map
from utils.position import Position

class Cartographer:
    def __init__(self, map_to_update, lasers_distance = 0.15, min_increment = 0.015, increment = 0.15, max_distance = 40, safe_distance_obstacle = 5, safe_distance_empty = 10):
        self.__map = map_to_update
        self.__lasers_distance = lasers_distance
        self.__max_distance = max_distance
        self.__min_increment = min_increment
        self.__increment = increment
        self.__safe_distance_obstacle = safe_distance_obstacle
        self.__safe_distance_empty = safe_distance_empty
        
    def update(self, robot_pos, lasers):
        lasers_pos_x = robot_pos.x + self.__lasers_distance * cos(robot_pos.angle)
        lasers_pos_y = robot_pos.y + self.__lasers_distance * sin(robot_pos.angle)
        lasers_cell = self.__map.to_grid_pos(Position(lasers_pos_x, lasers_pos_y))
        real_lasers_cell = self.__map.to_real_pos(lasers_cell)
        count = 0
        for laser in lasers:
            count += 1
            if count % 2 == 0:
                angle = robot_pos.angle + laser.angle
                laser_hit = Position(lasers_pos_x + laser.echoe * cos(angle), lasers_pos_y + laser.echoe * sin(angle))
                hit_cell = self.__map.to_grid_pos(laser_hit)
                cells = bresenham_line(lasers_cell.x, lasers_cell.y, hit_cell.x, hit_cell.y)
                for cell in cells:
                    if self.__map.is_in_bound(cell):
                        if cell.x == hit_cell.x and cell.y == hit_cell.y:
                            if laser.echoe < self.__max_distance - self.__safe_distance_obstacle:
                                inc_iro_certainty = self.__min_increment if self.__map.is_empty(cell) else self.__increment
                                inc_factor_iro_dist = (1.0 - (laser.echoe / self.__max_distance))
                                self.__map.grid[cell.x][cell.y] += inc_factor_iro_dist * inc_iro_certainty 
                                if self.__map.grid[cell.x][cell.y] > 1.0:
                                    self.__map.grid[cell.x][cell.y] = 1.0
                        else:
                            real_cell = self.__map.to_real_pos(cell)
                            distance = hypot(real_cell.x - real_lasers_cell.x, real_cell.y - real_lasers_cell.y)
                            if distance < self.__max_distance - self.__safe_distance_empty:
                                inc_iro_certainty = self.__min_increment if self.__map.is_obstacle(cell) else self.__increment
                                inc_factor_iro_dist = (1.0 - (distance / self.__max_distance))
                                self.__map.grid[cell.x][cell.y] -= inc_factor_iro_dist * inc_iro_certainty
                                if self.__map.grid[cell.x][cell.y] < 0.0:
                                    self.__map.grid[cell.x][cell.y] = 0.0
