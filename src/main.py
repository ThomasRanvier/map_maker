from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from planning.goal_planner import GoalPlanner
from planning.path_planner import PathPlanner
from utils.position import Position
from utils.utils import distance_2
from multiprocessing import Queue, Process
import time

def run_show_map(queue_show_map, robot_map, show_map_sleep_time):
    show_map = ShowMap(robot_map)
    while True:
        while not queue_show_map.empty():
            robot_pos, frontiers, goal_point, path = queue_show_map.get()
        show_map.update(robot_map.to_grid_pos(robot_pos), frontiers=frontiers, goal_point=goal_point, path=path)
        time.sleep(show_map_sleep_time)

def is_goal_reached(goal_point, robot_map, robot_pos, distance_to_trigger_goal_m, size_of_cell_in_meter):
    if goal_point != None:
        dist_2 = distance_2(robot_map.to_grid_pos(robot_pos), goal_point)
        trigger_2 = (distance_to_trigger_goal_m * (1.0 / size_of_cell_in_meter))**2
        goal_reached = (dist_2 <= trigger_2)
        return goal_reached
    return False

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter
    distance_to_trigger_goal_m = 6
    show_map_sleep_time = 0.5

    robot = Robot(url)
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    goal_planner = GoalPlanner(robot_map)
    path_planner = PathPlanner(robot_map)
    cartographer = Cartographer(robot_map)

    queue_show_map = Queue()
    show_map_process = Process(target=run_show_map, args=(queue_show_map, robot_map, show_map_sleep_time))
    show_map_process.daemon = True
    show_map_process.start()

    frontiers = None
    goal_point = None
    path = None
    start = time.time()
    delay = 2

    while True:
        robot_pos = robot.position
        robot_lasers = robot.lasers
        cartographer.update(robot_pos, robot_lasers)
        #show_map.update(robot_map.to_grid_pos(robot_pos), frontiers=frontiers, goal_point=goal_point)
        goal_reached = is_goal_reached(goal_point, robot_map, robot_pos, distance_to_trigger_goal_m, size_of_cell_in_meter)
        if time.time() - start >= delay or goal_reached:
            goal_point, frontiers = goal_planner.get_goal_point(robot_pos)
            path = path_planner.get_path(robot_pos, goal_point)
            start = time.time()
            delay = 10
        queue_show_map.put([robot_pos, frontiers, goal_point, path])
