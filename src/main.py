from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from planning.goal_planner import GoalPlanner
from planning.path_planner import PathPlanner
from utils.position import Position
from utils.utils import distance_2
from controlling.controller import Controller
from multiprocessing import Queue, Process
import time
import logging

logging.basicConfig(format='%(levelname)s:%(name)s:%(funcName)s: %(message)s' ,level=logging.INFO)
logger = logging.getLogger(__name__)

def is_goal_reached(goal_point, robot_cell, distance_to_trigger_goal_m, size_of_cell_in_meter):
    if goal_point != None:
        dist_2 = distance_2(robot_cell, goal_point)
        trigger_2 = (distance_to_trigger_goal_m * (1.0 / size_of_cell_in_meter))**2
        goal_reached = (dist_2 <= trigger_2)
        if goal_reached:
            logger.info('Goal reached')
        return goal_reached
    return False

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter
    distance_to_trigger_goal_m = 6
    show_map_sleep_time = 0.5
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)

    robot = Robot(url)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    controller = Controller(robot, robot_map)
    goal_planner = GoalPlanner(robot_map)
    #path_planner = PathPlanner(robot_map)
    cartographer = Cartographer(robot_map)

    show_map = ShowMap(robot_map.grid)

    frontiers = None
    goal_point = None
    path = None
    start = time.time()
    delay = 10

    controller.turn_around()
    while True:
        robot_pos = robot.position
        robot_cell = robot_map.to_grid_pos(robot_pos)
        robot_lasers = robot.lasers
        cartographer.update(robot_pos, robot_lasers)
        controller.go_to_goal_point(robot_cell, goal_point)
        goal_reached = is_goal_reached(goal_point, robot_cell, distance_to_trigger_goal_m, size_of_cell_in_meter)
        if time.time() - start >= delay or goal_reached:
            controller.stop()
            goal_point, frontiers = goal_planner.get_goal_point(robot_cell)
            #path = path_planner.get_path(robot_pos, goal_point)
            start = time.time()
            delay = 20
        show_map.update(robot_map, robot_map.to_grid_pos(robot_pos), frontiers=frontiers, goal_point=goal_point)
