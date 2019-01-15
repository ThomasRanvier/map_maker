from robot import Robot
from map import Map
from goal_planner import GoalPlanner
from path_planner import PathPlanner
from position import Position
from utils import distance_2
from controller import Controller
from potential_field import PotentialField
from multiprocessing import Queue, Process
from jobs import show_map_job, cartographer_job, frontiers_limiter_job
from math import hypot
import time
import logging
import sys
import argparse
import signal

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="The url of the MRDS server with the port, the format is url:port")
parser.add_argument("lower_left_pos_x", type=int, help="The X coordinate of the lower left position.")
parser.add_argument("lower_left_pos_y", type=int, help="The Y coordinate of the lower left position.")
parser.add_argument("upper_right_pos_x", type=int, help="The X coordinate of the upper right position.")
parser.add_argument("upper_right_pos_y", type=int, help="The Y coordinate of the upper right position.")
parser.add_argument("show_gui", type=int, help="1 if you want to show the GUI, 0 otherwise.")
args = parser.parse_args()

logging.basicConfig(format='%(levelname)s:%(name)s:%(funcName)s: %(message)s' ,level=logging.INFO)
logger = logging.getLogger(__name__)

cartographer_d, show_map_d, frontiers_limiter_d = None, None, None

def sigint_handler(sig, frame):
    """
    Handle the Ctrl-C (SIGINT) signal. Terminate all subworkers.
    """
    cartographer_d.terminate()
    show_map_d.terminate()
    frontiers_limiter_d.terminate()
    sys.exit(1)

def update_path(path, robot_cell, distance_to_trigger_goal):
    """
    Update the path depending on if the robot has progressed in it or not.
    :param path: The path to follow.
    :type path: A list of Position objects.
    :param robot_cell: The position of the robot in the grid.
    :type robot_cell: Position
    :param distance_to_trigger_goal: Distance under which the robot triggers the goal.
    :type distance_to_trigger_goal: float
    """
    if path != []:
        has_progressed = False
        for i in range(len(path) - 1, -1, -1):
            dist = hypot(path[i].x - robot_cell.x, path[i].y - robot_cell.y)
            has_progressed = (dist <= distance_to_trigger_goal)
            if has_progressed:
                for ii in range(i, -1, -1):
                    path.pop(ii)
                break
        if path == []:
            logger.info('Has finished')
    return path

if __name__ == '__main__':
    url = args.url
    url.replace('http://', '')
    robot = Robot(url)
    controller = Controller(robot)
    try:
        controller.stop()
        size_of_cell_in_meter = 0.5
        scale = 1 / size_of_cell_in_meter
        distance_to_trigger_goal_m = 3.0
        distance_between_subgoals_m = 5.0
        lower_left_pos = Position(args.lower_left_pos_x, args.lower_left_pos_y)
        upper_right_pos = Position(args.upper_right_pos_x, args.upper_right_pos_y)
        path_planning_delay = 14

        queue_cartographer = Queue(500)
        queue_sm_map = Queue(500)
        queue_sm_optionals = Queue(500)
        queue_fl_current_frontier = Queue(500)
        queue_fl_ignored_cells = Queue(500)

        robot_map = Map(lower_left_pos, upper_right_pos, scale)
        potential_field = PotentialField(robot)
        goal_planner = GoalPlanner(queue_fl_current_frontier, queue_fl_ignored_cells)
        path_planner = PathPlanner(distance_to_trigger_goal_m * scale, distance_between_subgoals_m * scale)

        cartographer_d = Process(target=cartographer_job, args=(queue_cartographer, queue_sm_map, robot_map, robot))
        cartographer_d.daemon = True
        cartographer_d.start()

        show_map_d = Process(target=show_map_job, args=(queue_sm_map, queue_sm_optionals, robot_map, robot, args.show_gui == 1))
        show_map_d.daemon = True
        show_map_d.start()

        frontiers_limiter_d = Process(target=frontiers_limiter_job, args=(queue_fl_current_frontier, queue_fl_ignored_cells, robot))
        frontiers_limiter_d.daemon = True
        frontiers_limiter_d.start()
        
        frontiers = None
        path = []
        forces = None
        over = False
        start_path_planning = 0

        signal.signal(signal.SIGINT, sigint_handler)

        controller.turn_around()
        time.sleep(10)
        while not over:
            start_loop = time.time()
            while not queue_cartographer.empty():
                robot_map = queue_cartographer.get()
            robot_pos = robot.position
            robot_cell = robot_map.to_grid_pos(robot_pos)
            if path != []:
                forces = potential_field.get_forces(robot_cell, path[0], robot_map)
                controller.apply_force(forces['gen_force'], robot_pos)
            path = update_path(path, robot_cell, distance_to_trigger_goal_m * scale)
            if path == [] or time.time() - start_path_planning >= 5:
                start_path_planning = time.time()
                controller.stop()
                robot_cell = robot_map.to_grid_pos(robot.position)
                goal_point, frontiers = goal_planner.get_goal_point(robot_cell, robot_map)
                path = path_planner.get_path(robot_cell, robot_map, goal_point)
                if path == []:
                    logger.info('Over')
                    over = True
            queue_sm_optionals.put([frontiers, forces, path])
            sleep = 0.1 - (time.time() - start_loop)
            if sleep > 0:
                time.sleep(sleep)
    except:
        print('Cannot connect to MRDS server.', sys.stderr)
