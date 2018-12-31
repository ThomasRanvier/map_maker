from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from planning.goal_planner import GoalPlanner
from utils.position import Position
import time

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter

    robot = Robot(url)
    lower_left_pos = Position(-50.0, -50.0)
    upper_right_pos = Position(50.0, 50.0)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    goal_planner = GoalPlanner(robot_map)
    cartographer = Cartographer(robot_map)
    show_map = ShowMap(robot_map)
    frontiers = None
    goal_point = None
    start = 0

    while True:
        robot_pos = robot.position
        robot_lasers = robot.lasers
        cartographer.update(robot_pos, robot_lasers)
        show_map.update(robot_map.to_grid_pos(robot_pos), frontiers=frontiers, goal_point=goal_point)
        if time.time() - start >= 5:
            goal_point, frontiers = goal_planner.get_goal_point(robot_pos)
            start = time.time()

