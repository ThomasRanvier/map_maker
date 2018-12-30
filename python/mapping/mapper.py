from utils.utils import bresenham_line
from math import hypot, cos, sin, pi
from mapping.map import Map
from utils.position import Position

class Mapper:
    def __init__(self, map_to_update, lasers_distance = 0.15, min_increase = 0.04, increase = 0.15, max_distance = 40):
        self.__map = map_to_update
        self.__lasers_distance = lasers_distance
        self.__max_distance = max_distance
        self.__min_increase = min_increase
        self.__increase = increase
        
    def update(self, robot_pos, lasers):
        lasers_pos_x = robot_pos.x + self.__lasers_distance * cos(robot_pos.angle)
        lasers_pos_y = robot_pos.y + self.__lasers_distance * sin(robot_pos.angle)
        lasers_cell = self.__map.to_grid_pos(Position(lasers_pos_x, lasers_pos_y))
        real_lasers_cell = self.__map.to_real_pos(lasers_cell)
        robot_angle = robot_pos.angle
        while robot_angle > pi:
            robot_angle -= pi
        while robot_angle < -pi:
            robot_angle += pi
        for laser in lasers:
            angle = robot_angle + laser.angle
            laser_hit = Position(lasers_pos_x + laser.echoe * cos(angle), lasers_pos_y + laser.echoe * sin(angle))
            hit_cell = self.__map.to_grid_pos(laser_hit)
            cells = bresenham_line(lasers_cell.x, lasers_cell.y, hit_cell.x, hit_cell.y)
            for cell in cells:
                if self.__map.is_in_bound(cell):
                    inc = max(self.__min_increase, self.__increase * (abs(self.__map.grid[cell.x][cell.y] - 0.5) * 2.0 * self.__increase))
                    if cell.x == hit_cell.x and cell.y == hit_cell.y:
                        if laser.echoe < self.__max_distance:
                            self.__map.grid[hit_cell.x][hit_cell.y] += inc
                            if self.__map.grid[hit_cell.x][hit_cell.y] > 1.0:
                                self.__map.grid[hit_cell.x][hit_cell.y] = 1.0
                    else:
                        self.__map.grid[cell.x][cell.y] -= inc
                        if self.__map.grid[cell.x][cell.y] < 0.0:
                            self.__map.grid[cell.x][cell.y] = 0.0
