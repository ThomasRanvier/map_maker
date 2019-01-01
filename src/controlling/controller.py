from logging import getLogger
from math import hypot, atan2, cos, sin, inf
from utils.utils import filled_midpoint_circle

logger = getLogger('controller')

class Controller:
    def __init__(self, robot, robot_map):
        self.__map = robot_map
        self.__robot = robot
    
    def go_to_goal_point(self, robot_cell, goal_point):
        if goal_point == None:
            return
        pass

    def attractive_force(self, robot_cell, goal_point):
        if goal_point == None:
            return None
        length = 0.4 * hypot(robot_cell.x - goal_point.x, robot_cell.y - goal_point.y)
        dx = goal_point.x - robot_cell.x
        dy = goal_point.y - robot_cell.y
        angle = atan2(dy, dx)
        return {'dx': length * cos(angle), 'dy': length * sin(angle)}

    def repulsive_force(self, robot_cell, radius = 6, max_obstacles = 5):
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
            dist = hypot(robot_cell.x - obstacle.x, robot_cell.y - obstacle.y)
            length = (radius * 2) - dist
            dx = obstacle.x - robot_cell.x
            dy = obstacle.y - robot_cell.y
            angle = atan2(dy, dx)
            result['dx'] += -length * cos(angle)
            result['dy'] += -length * sin(angle)
        if result['dx'] == 0 and result['dy'] == 0:
            result = None
        return result

    def turn_around(self):
        logger.info('Make the robot turn around')
        self.__robot.post_speed(1, 1)

    def stop(self):
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
