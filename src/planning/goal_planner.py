from utils.position import Position
from utils.utils import von_neumann_neighbourhood, moore_neighbourhood, distance_2
from math import inf

class GoalPlanner:
    def __init__(self, robot_map, min_frontier_points = 20):
        self.__map = robot_map
        self.__min_frontier_points = min_frontier_points

    def get_goal_point(self, robot_pos):
        frontiers = self.__get_frontiers(robot_pos)
        if frontiers:
            closest_frontier = self.__find_closest_frontier(frontiers, robot_pos)
            goal_point = self.__find_centroid(closest_frontier)
            return (goal_point, frontiers)
        return (None, None)

    def __find_centroid(self, frontier):
        count = 0.0
        x_sum = 0.0
        y_sum = 0.0
        for point in frontier:
            x_sum += point.x
            y_sum += point.y
            count += 1.0
        return Position(x_sum / count, y_sum / count)

    def __find_closest_frontier(self, frontiers, robot_pos):
        closest_frontier = frontiers[0]
        if len(frontiers) == 1:
            return closest_frontier
        robot_cell = self.__map.to_grid_pos(Position(robot_pos.x, robot_pos.y))
        min_distance = inf
        for frontier in frontiers:
            for point in frontier:
                dist = distance_2(robot_cell, point)
                if dist < min_distance:
                    min_distance = dist
                    closest_frontier = frontier
        return closest_frontier

    def __get_frontiers(self, robot_pos):
        """
        https://arxiv.org/pdf/1806.03581.pdf
        """
        robot_cell = self.__map.to_grid_pos(Position(robot_pos.x, robot_pos.y))
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
        for n in moore_neighbourhood(cell, self.__map.grid_width, self.__map.grid_height):
            if self.__map.is_empty(n):
                return True
        return False
    
    def __is_frontier_point(self, cell):
        if self.__map.is_unknown(cell):
            for neighbour in von_neumann_neighbourhood(cell, self.__map.grid_width, self.__map.grid_height):
                if self.__map.is_empty(neighbour):
                    return True
        return False
