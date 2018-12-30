from utils.utils import bresenham_line
from math import hypot, cos, sin, pi
from mapping.map import Map
from utils.position import Position

class Mapper:
    def __init__(self, map_to_update, lasers_distance = 0.15, p_max = 0.98, min_increase = 0.01, increase = 0.1, max_distance = 40):
        self.__map = map_to_update
        self.__lasers_distance = lasers_distance
        self.__max_distance = max_distance
        self.__p_max = p_max
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
                    inc = self.__increase(abs(self.__map.grid[cell.x][cell.y] - 0.5) * 2.0 * self.__increase)
                    if cell.x == hit_cell.x and cell.y == hit_cell.y:
                        if laser.echoe < self.__max_distance:
                            self.__map.grid[hit_cell.x][hit_cell.y] += inc
                            if self.__map.grid[hit_cell.x][hit_cell.y] > 1.0:
                                self.__map.grid[hit_cell.x][hit_cell.y] = 1.0
                        """
                        if laser.echoe <= self.__max_distance - 5:
                            occupied_probability = self.__occupied_probability(laser.echoe)
                            if not self.__map.grid[hit_cell.x][hit_cell.y] >= 0.7:
                                occupied_probability += self.__min_increase
                            self.__map.grid[hit_cell.x][hit_cell.y] = self.__bayesian_probability(1 - occupied_probability, self.__map.grid[hit_cell.x][hit_cell.y])"""
                    else:
                        self.__map.grid[cell.x][cell.y] -= inc
                        if self.__map.grid[cell.x][cell.y] < 0.0:
                            self.__map.grid[cell.x][cell.y] = 0.0
                        """
                        real_cell = self.__map.to_real_pos(cell)
                        distance = hypot(real_cell.x - real_lasers_cell.x, real_cell.y - real_lasers_cell.y)    
                        if distance <= self.__max_distance - 10:
                            occupied_probability = self.__occupied_probability(distance)
                            self.__map.grid[cell.x][cell.y] = self.__bayesian_probability(occupied_probability, self.__map.grid[cell.x][cell.y])"""

    def __bayesian_probability(self, occupied_probability, previous_probabilty):
        empty_probability = 1 - occupied_probability
        empty_previous_probability = 1 - previous_probabilty
        return ((occupied_probability * previous_probabilty) / 
                (occupied_probability * previous_probabilty + empty_probability * empty_previous_probability))
    
    def __occupied_probability(self, distance):
        return ((self.__max_distance - distance) / self.__max_distance) / 2 * self.__p_max
