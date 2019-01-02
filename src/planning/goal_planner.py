from utils.position import Position
from utils.utils import von_neumann_neighbourhood, moore_neighbourhood, distance_2, centroid
from math import inf
from logging import getLogger

logger = getLogger('goal_planner')

class GoalPlanner:
    """
    Class that implement a GoalPlanner, used to find a new goal from the frontiers between the explored and unknown world.
    """

    def __init__(self, robot_map, min_frontier_points = 20):
        """
        Instantiates a GoalPlanner.
        :param robot_map: The map of the environment.
        :type robot_map: Map
        :param min_frontier_points: Minimum points in a frontier to be relevant.
        :type min_frontier_points: integer
        """
        self.__map = robot_map
        self.__min_frontier_points = min_frontier_points

    def get_goal_point(self, robot_cell):
        """
        Function that gives the user a new goal point by choosing the centroid of the closest frontier.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :return: The goal point and the frontiers.
        :rtype: A set of one Position and a 2D list of Position objects.
        """
        logger.info('Search new goal')
        frontiers = self.__get_frontiers(robot_cell)
        if frontiers:
            closest_frontier = self.__find_closest_frontier(frontiers, robot_cell)
            goal_point = centroid(closest_frontier)
            logger.info('New goal defined')
            return (goal_point, frontiers)
        logger.info('No frontiers found')
        return (None, None)

    def __find_closest_frontier(self, frontiers, robot_cell):
        """
        Function that finds the closest frontier in regard of the robot.
        :param frontiers: A list of the frontiers.
        :type frontiers: A 2D list of Position objects.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :return: The closest frontier from the robot.
        :rtype: A list of Position objects.
        """
        logger.info('Search closest frontier')
        closest_frontier = frontiers[0]
        if len(frontiers) == 1:
            return closest_frontier
        min_distance = inf
        for frontier in frontiers:
            for point in frontier:
                dist = distance_2(robot_cell, point)
                if dist < min_distance:
                    min_distance = dist
                    closest_frontier = frontier
        return closest_frontier

    def __get_frontiers(self, robot_cell):
        """
        https://arxiv.org/pdf/1806.03581.pdf
        This is an implementation of the Wavefront Frontier Finder algorithm that can be found in the scientific paper above.
        Gives the frontiers between the explored and unknown world that could be reached by the robot.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :return: A list of all the frontiers.
        :rtype: A 2D list of Position objects.
        """
        logger.info('Search frontiers')
        frontiers = []
        queue_m = []
        map_open = set([])
        map_close = set([])
        frontier_open = set([])
        frontier_close = set([])
        queue_m.append(robot_cell)
        map_open.add(robot_cell)
        while queue_m:
            p = queue_m.pop(0)
            if p in map_close:
                continue
            if self.__is_frontier_point(p):
                queue_f = []
                frontier = set([])
                queue_f.append(p)
                frontier_open.add(p)
                while queue_f:
                    q = queue_f.pop(0)
                    if q in map_close and q in frontier_close:
                        continue
                    if self.__is_frontier_point(q):
                        frontier.add(q)
                        for w in moore_neighbourhood(q, self.__map.grid_width, self.__map.grid_height):
                            if w not in frontier_open and w not in map_close and w not in frontier_close:
                                queue_f.append(w)
                                frontier_open.add(w)    
                    frontier_close.add(q)
                if len(frontier) >= self.__min_frontier_points:
                    frontiers.append(frontier)
                for cell in frontier:
                    map_close.add(cell)
            for v in moore_neighbourhood(p, self.__map.grid_width, self.__map.grid_height):
                if v not in map_open and v not in map_close and self.__has_open_neighbour(v):
                    queue_m.append(v)
                    map_open.add(v)
            map_close.add(p)
        return frontiers
                            
    def __has_open_neighbour(self, cell):
        """
        Tells if the selected cell has an open (empty) neighbour or not.
        :param cell: Cell in the grid.
        :type cell: Position
        :return: True if the cell has an open neighbour, False otherwise.
        :rtype: boolean
        """
        for n in moore_neighbourhood(cell, self.__map.grid_width, self.__map.grid_height):
            if self.__map.is_empty(n):
                return True
        return False
    
    def __is_frontier_point(self, cell):
        """
        Tells if the selected cell is a frontier point or not.
        :param cell: Cell in the grid.
        :type cell: Position
        :return: True if the cell is a frontier point, False otherwise.
        :rtype: boolean
        """
        if self.__map.is_unknown(cell):
            for neighbour in von_neumann_neighbourhood(cell, self.__map.grid_width, self.__map.grid_height):
                if self.__map.is_empty(neighbour):
                    return True
        return False
