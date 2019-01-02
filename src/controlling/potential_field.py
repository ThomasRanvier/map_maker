from math import hypot, atan2, cos, sin, inf
from utils.utils import filled_midpoint_circle
from logging import getLogger

logger = getLogger('potential_field')

class PotentialField:
    """
    Class that implements a PotentialField, used to compute the force to apply to the robot to make it reach the goal point while avoiding obstacles.
    """

    def __init__(self, robot, weight_attr = 0.5, weight_rep = 4, radius_obs = 10, max_obs = 10, trigger_obs = 0.75):
        """
        Instantiates a PotentialField.
        :param robot: The robot.
        :type robot: Robot
        :param weight_attr: The weight to apply to the attractive force.
        :type weight_attr: float
        :param weight_rep: The weight to apply to the repulsive force.
        :type weight_rep: float
        :param radius_obs: Radius of the circle to analyze around the robot for obstacles.
        :type radius_obs: integer
        :param max_obs: The maximum number of obstacles that will influence the repulsive force.
        :type max_obs: integer
        :param trigger_obs: The minimum value to be considered as a relevant obstacle here.
        :type trigger_obs: float
        """
        self.__robot = robot
        self.__weight_attr = weight_attr
        self.__weight_rep = weight_rep
        self.__radius_obs = radius_obs
        self.__trigger_obs = trigger_obs
        self.__max_obs = max_obs

    def get_forces(self, robot_cell, goal_point, robot_map):
        """
        Gives the attractive, repulsive and general forces to apply to the robot.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param robot_map: The map of the environment
        :type robot_map: Map
        :param goal_point: Position of the goal of the robot in the grid.
        :type goal_point: Position
        :return: The 3 forces.
        :rtype: A dictionary containing the 3 forces, which also are dictionaries.
        """
        forces = {'gen_force': None, 'attr_force': None, 'rep_force': None}
        forces['attr_force'] = self.__get_attractive_force(robot_cell, goal_point)
        forces['rep_force'] = self.__get_repulsive_force(robot_cell, robot_map)
        forces['gen_force'] = {'x': forces['attr_force']['x'] + forces['rep_force']['x'], 
                                'y': forces['attr_force']['y'] + forces['rep_force']['y']}
        return forces

    def __get_attractive_force(self, robot_cell, goal_point):
        """
        Gives the attractive force to apply to the robot.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param goal_point: Position of the goal of the robot in the grid.
        :type goal_point: Position
        :return: The attractive force.
        :rtype: A dictionary containing the coordinates of the attractive vector.
        """
        if goal_point == None:
            return {'x': 0, 'y': 0}
        length = self.__weight_attr * hypot(robot_cell.x - goal_point.x, robot_cell.y - goal_point.y)
        dx = goal_point.x - robot_cell.x
        dy = goal_point.y - robot_cell.y
        angle = atan2(dy, dx)
        return {'x': length * cos(angle), 'y': length * sin(angle)}

    def __get_repulsive_force(self, robot_cell, robot_map):
        """
        Gives the repulsive force to apply to the robot.
        Obtained by summing the repulsive forces applied by the 5 closest obstacles (if they exist) to the robot.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param robot_map: The map of the environment
        :type robot_map: Map
        :return: The repulsive force.
        :rtype: A dictionary containing the coordinates of the repulsive vector.
        """
        circle = filled_midpoint_circle(robot_cell.x, robot_cell.y, self.__radius_obs)
        closest_obstacles = [None] * self.__max_obs
        min_dists = [inf] * self.__max_obs
        for point in circle:
            if robot_map.is_in_bound(point) and robot_map.grid[point.x][point.y] >= 0.75:
                dist = hypot(robot_cell.x - point.x, robot_cell.y - point.y)
                for i in range(self.__max_obs):
                    if dist < min_dists[i]:
                        for ii in range(self.__max_obs - 1, i + 2, -1):
                            min_dists[ii] = min_dists[ii - 1]
                            closest_obstacles[ii] = closest_obstacles[ii - 1]
                        min_dists[i] = dist
                        closest_obstacles[i] = point
                        break
        result = {'x': 0, 'y': 0}
        for obstacle in closest_obstacles:
            if obstacle != None:
                dist = hypot(robot_cell.x - obstacle.x, robot_cell.y - obstacle.y)
                length = (abs(self.__radius_obs - dist) / self.__radius_obs) * self.__weight_rep
                dx = obstacle.x - robot_cell.x
                dy = obstacle.y - robot_cell.y
                angle = atan2(dy, dx)
                result['x'] += -length * cos(angle)
                result['y'] += -length * sin(angle)
        return result
