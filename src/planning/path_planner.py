from utils.position import Position
from logging import getLogger

logger = getLogger('path_planner')

class PathPlanner:
    def __init__(self, robot_map, attractive_pot_gain = 5.0, repulsive_pot_gain = 100.0, max_obstacles = 5):
        self.__map = robot_map

    def get_path(self, robot_cell, goal_point):
        
        return None
