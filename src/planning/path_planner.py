from utils.utils import distance_2, von_neumann_neighbourhood
from math import inf
from logging import getLogger

logger = getLogger('path_planner')

class PathPlanner:
    """
    Class that implements an algorithm of path planning, used to smooth out the potential field controller.
    """

    def __init__(self, trigger_dist, dist_between_subgoals , max_depth = 500):
        """
        Instantiates a PathPlanner.
        :param trigger_dist: Trigger distance from the goal where we can stop.
        :type trigger_dist: float
        :param dist_between_subgoals: Distance between each subgoals.
        :type dist_between_subgoals: float
        :param max_depth: Maximum depth of the algorithm.
        :type max_depth: integer
        """
        self.__trigger_dist = trigger_dist ** 2
        self.__max_depth = max_depth
        self.__dist_between_subgoals = dist_between_subgoals ** 2

    def get_path(self, robot_cell, robot_map, goal_point):
        """
        Gives a path that tries to avoid the obstacles while going to the goal point.
        :param robot_cell: Cell of the robot.
        :type robot_cell: Position
        :param robot_map: Map of the environment.
        :type robot_map: Map
        :param goal_point: Cell of the goal.
        :type goal_point: Position
        """
        if goal_point == None:
            return []
        closed_set = set([])
        open_set = set([robot_cell])
        came_from = {}
        g_score = {robot_cell: 0}
        f_score = {robot_cell: distance_2(robot_cell, goal_point)}
        depth = 1
        current = None
        while not len(open_set) == 0:
            min_score = inf
            for cell in open_set:
                if f_score[cell] < min_score:
                    min_score = f_score[cell]
                    current = cell
            if distance_2(current, goal_point) <= self.__trigger_dist or depth >= self.__max_depth:
                logger.info('Path defined')
                return self.__reconstruct_path(came_from, current)
            open_set.remove(current)
            closed_set.add(current)
            for neighbour in von_neumann_neighbourhood(current, robot_map.grid_width, robot_map.grid_height):
                if robot_map.is_unknown(neighbour) or robot_map.is_obstacle(neighbour):
                    continue
                tentative_g_score = g_score[current] + distance_2(current, neighbour)
                if neighbour in closed_set and tentative_g_score >= g_score[neighbour]:
                    continue
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + distance_2(neighbour, goal_point)
                open_set.add(neighbour)
            depth += 1
        logger.info('Impossible to define path')
        return self.__reconstruct_path(came_from, current)

    def __reconstruct_path(self, came_from, current):
        """
        Function used to reconstruct the path.
        :param came_from: The came_from list from the A* algorithm.
        :type came_from: list
        :param current: Current point from the A* algortihm.
        :type current: Position
        """
        path = []
        path.append(current)
        last = current
        while current in came_from:
            if distance_2(current, last) >= self.__dist_between_subgoals:
                path.append(current)
                last = current
            current = came_from[current]
        return path[::-1]
