from position import Position
from utils import von_neumann_neighbourhood, moore_neighbourhood, distance_2, centroid, get_deltas, bresenham_line
from math import inf, hypot
from logging import getLogger

logger = getLogger('goal_planner')

class GoalPlanner:
    """
    Class that implement a GoalPlanner, used to find a new goal from the frontiers between the explored and unknown world.
    """

    def __init__(self, queue_fl_current_frontier, queue_fl_ignored_cells, min_frontier_points = 20):
        """
        Instantiates a GoalPlanner.
        :param queue_fl_current_frontier: The queue where to put the closest frontier found.
        :type queue_fl_current_frontier: Queue
        :param queue_fl_ignored_cells: The queue where to get the cells to ignore.
        :type queue_fl_ignored_cells: Queue
        :param min_frontier_points: Minimum points in a frontier to be relevant.
        :type min_frontier_points: integer
        """
        self.__queue_fl_current_frontier = queue_fl_current_frontier
        self.__queue_fl_ignored_cells = queue_fl_ignored_cells
        self.__min_frontier_points = min_frontier_points
        self.__ignored_cells = None

    def get_goal_point(self, robot_cell, robot_map):
        """
        Function that gives the user a new goal point by choosing the centroid of the closest frontier.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param robot_map: The map of the environment.
        :type robot_map: Map
        :return: The goal point and the frontiers.
        :rtype: A set of one Position and a 2D list of Position objects.
        """
        logger.info('Search new goal')
        frontiers = self.__get_frontiers(robot_cell, robot_map)
        if frontiers:
            closest_frontier = self.__find_closest_frontier(frontiers, robot_cell)#self.__find_biggest_frontier(frontiers, robot_cell)
            #most_accessible_frontier = self.__find_most_accessible_frontier(frontiers, robot_cell, robot_map)
            goal_point = centroid(closest_frontier)
            logger.info('New goal defined')
            return (goal_point, frontiers)
        logger.info('No frontiers found')
        return (None, None)

    def __find_closest_frontier(self, frontiers, robot_cell):
        """
        Function that finds the closest frontier in regard of the robot and of the centroid of each frontier.
        :param frontiers: A list of the frontiers.
        :type frontiers: A 2D list of Position objects.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :return: The closest frontier from the robot.
        :rtype: A list of Position objects.
        """
        closest_frontier = frontiers[0]
        if len(frontiers) == 1:
            self.__queue_fl_current_frontier.put(closest_frontier)
            return closest_frontier
        logger.info('Search closest frontier')
        min_distance = inf
        for frontier in frontiers:
            dist = distance_2(robot_cell, centroid(frontier))
            if dist < min_distance:
                min_distance = dist
                closest_frontier = frontier
        self.__queue_fl_current_frontier.put(closest_frontier)
        return closest_frontier

    def __find_biggest_frontier(self, frontiers, robot_cell, max_distance = 150):
        """
        Function that finds the biggest frontier (Under max_distance).
        :param frontiers: A list of the frontiers.
        :type frontiers: A 2D list of Position objects.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param max_distance: The maximum distance under which the frontiers are considered.
        :type max_distance: integer
        :return: The biggest frontier.
        :rtype: A list of Position objects.
        """
        biggest_frontier = frontiers[0]
        if len(frontiers) == 1:
            self.__queue_fl_current_frontier.put(biggest_frontier)
            return biggest_frontier
        logger.info('Search biggest frontier')
        max_size = -inf
        for frontier in frontiers:
            middle = centroid(frontier)
            if hypot(robot_cell.x - middle.x, middle.y - robot_cell.y) <= max_distance:
                delta_x, delta_y = get_deltas(list(frontier), len(frontier))
                if delta_x + delta_y > max_size:
                    max_size = delta_x + delta_y
                    biggest_frontier = frontier
        self.__queue_fl_current_frontier.put(biggest_frontier)
        return biggest_frontier

    def __find_most_accessible_frontier(self, frontiers, robot_cell, robot_map):
        most_accessible_frontier = frontiers[0]
        if len(frontiers) == 1:
            self.__queue_fl_current_frontier.put(most_accessible_frontier)
            return most_accessible_frontier 
        logger.info('Search most accessible frontier.')
        min_obs = inf
        for frontier in frontiers:
            middle = centroid(frontier)
            line = bresenham_line(robot_cell.x, robot_cell.y, int(middle.x), int(middle.y))
            obs_count = 0
            for point in line:
                if not robot_map.is_empty(point):
                    if robot_map.is_unknown(point):
                        obs_count += 1
                    else:
                        obs_count += 50
            if obs_count < min_obs:
                min_obs = obs_count
                most_accessible_frontier = frontier
        self.__queue_fl_current_frontier.put(most_accessible_frontier)
        return most_accessible_frontier

    def __get_frontiers(self, robot_cell, robot_map):
        """
        https://arxiv.org/pdf/1806.03581.pdf
        This is an implementation of the Wavefront Frontier Finder algorithm that can be found in the scientific paper above.
        Gives the frontiers between the explored and unknown world that could be reached by the robot.
        :param robot_cell: Position of the robot in the grid.
        :type robot_cell: Position
        :param robot_map: The map of the environment.
        :type robot_map: Map
        :return: A list of all the frontiers.
        :rtype: A 2D list of Position objects.
        """
        logger.info('Search frontiers')
        while not self.__queue_fl_ignored_cells.empty():
            self.__ignored_cells = self.__queue_fl_ignored_cells.get()
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
            if self.__is_frontier_point(p, robot_map):
                queue_f = []
                frontier = set([])
                queue_f.append(p)
                frontier_open.add(p)
                while queue_f:
                    q = queue_f.pop(0)
                    if q in map_close and q in frontier_close:
                        continue
                    if self.__is_frontier_point(q, robot_map):
                        if self.__ignored_cells == None:
                            frontier.add(q)
                        elif q not in self.__ignored_cells:
                            frontier.add(q)
                        for w in moore_neighbourhood(q, robot_map.grid_width, robot_map.grid_height):
                            if w not in frontier_open and w not in map_close and w not in frontier_close:
                                queue_f.append(w)
                                frontier_open.add(w)    
                    frontier_close.add(q)
                if len(frontier) >= self.__min_frontier_points:
                    frontiers.append(frontier)
                for cell in frontier:
                    map_close.add(cell)
            for v in moore_neighbourhood(p, robot_map.grid_width, robot_map.grid_height):
                if v not in map_open and v not in map_close and self.__has_open_neighbour(v, robot_map):
                    queue_m.append(v)
                    map_open.add(v)
            map_close.add(p)
        return frontiers
                            
    def __has_open_neighbour(self, cell, robot_map):
        """
        Tells if the selected cell has an open (empty) neighbour or not.
        :param cell: Cell in the grid.
        :type cell: Position
        :param robot_map: The map of the environment.
        :type robot_map: Map
        :return: True if the cell has an open neighbour, False otherwise.
        :rtype: boolean
        """
        for n in moore_neighbourhood(cell, robot_map.grid_width, robot_map.grid_height):
            if robot_map.is_empty(n):
                return True
        return False
    
    def __is_frontier_point(self, cell, robot_map):
        """
        Tells if the selected cell is a frontier point or not.
        :param cell: Cell in the grid.
        :type cell: Position
        :param robot_map: The map of the environment.
        :type robot_map: Map
        :return: True if the cell is a frontier point, False otherwise.
        :rtype: boolean
        """
        if robot_map.is_unknown(cell):
            for neighbour in von_neumann_neighbourhood(cell, robot_map.grid_width, robot_map.grid_height):
                if robot_map.is_empty(neighbour):
                    return True
        return False
