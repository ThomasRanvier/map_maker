from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from planning.goal_planner import GoalPlanner
from utils.position import Position
from utils.utils import distance_2
import time

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter

    robot = Robot(url)
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    goal_planner = GoalPlanner(robot_map)
    cartographer = Cartographer(robot_map)
    show_map = ShowMap(robot_map)
    frontiers = None
    goal_point = None
    path = None
    start = time.time()
    delay = 2

    while True:
        if goal_point != None:
            print('dist: ' + str(distance_2(robot_map.to_grid_pos(robot_pos), goal_point)))
        robot_pos = robot.position
        robot_lasers = robot.lasers
        cartographer.update(robot_pos, robot_lasers)
        show_map.update(robot_map.to_grid_pos(robot_pos), frontiers=frontiers, goal_point=goal_point)
        if time.time() - start >= delay or (goal_point != None and distance_2(robot_map.to_grid_pos(robot_pos), goal_point) <= 4):
            goal_point, frontiers = goal_planner.get_goal_point(robot_pos)
            #path = path_planner.get_path(robot_pos, goal_point)
            start = time.time()
            delay = 20

