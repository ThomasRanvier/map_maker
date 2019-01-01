from math import hypot, atan2, cos, sin, inf
from utils.utils import filled_midpoint_circle

logger = getLogger('potential_field')

class PotentialField:
    def __init__(self, robot, robot_map):
        self.__map = robot_map
        self.__robot = robot

    def get_forces(self, robot_cell, goal_point):
        logger.info('Calculate forces')
        forces = {'gen_force': None, 'attr_force': None, 'rep_force': None}
        forces['attr_force'] = self.__get_attractive_force(robot_cell, goal_point)
        forces['rep_force'] = self.__get_repulsive_force(robot_cell)
        logger.info('Calculate general force')
        forces['gen_force'] = {'dx': forces['attr_force']['dx'] + forces['rep_force']['dx'], 
                                'dy': forces['attr_force']['dy'] + forces['rep_force']['dy']}
        return forces

    def __get_attractive_force(self, robot_cell, goal_point, weight = 0.4):
        logger.info('Calculate attractive force')
        if goal_point == None:
            return {'dx': 0, 'dy': 0}
        length = weight * hypot(robot_cell.x - goal_point.x, robot_cell.y - goal_point.y)
        dx = goal_point.x - robot_cell.x
        dy = goal_point.y - robot_cell.y
        angle = atan2(dy, dx)
        return {'dx': length * cos(angle), 'dy': length * sin(angle)}

    def __get_repulsive_force(self, robot_cell, radius = 6, max_obstacles = 5, weight = 0.6):
        logger.info('Calculate repulsive force')
        circle = filled_midpoint_circle(robot_cell.x, robot_cell.y, radius)
        obstacles = []
        for point in circle:
            if self.__map.is_in_bound(point) and self.__map.grid[point.x][point.y] >= 0.75:
                obstacles.append(point)
        closest_obstacles = [None, None, None, None, None]
        if len(obstacles) <= max_obstacles:
            closest_obstacles = obstacles
        else:
            min_dists = [inf, inf, inf, inf, inf]
            for obstacle in obstacles:
                dist = hypot(robot_cell.x - obstacle.x, robot_cell.y - obstacle.y)
                for i in range(max_obstacles):
                    if dist < min_dists[i]:
                        for ii in range(max_obstacles - 1, i + 2, -1):
                            min_dists[ii] = min_dists[ii - 1]
                            closest_obstacles[ii] = closest_obstacles[ii - 1]
                        min_dists[i] = dist
                        closest_obstacles[i] = obstacle
                        break
        result = {'dx': 0, 'dy': 0}
        for obstacle in closest_obstacles:
            if obstacle != None:
                dist = hypot(robot_cell.x - obstacle.x, robot_cell.y - obstacle.y)
                length = ((radius * 2) - dist) * weight
                dx = obstacle.x - robot_cell.x
                dy = obstacle.y - robot_cell.y
                angle = atan2(dy, dx)
                result['dx'] += -length * cos(angle)
                result['dy'] += -length * sin(angle)
        return result
