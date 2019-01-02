from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from planning.goal_planner import GoalPlanner
from utils.position import Position
from utils.utils import distance_2
from controlling.controller import Controller
from controlling.potential_field import PotentialField
from multiprocessing import Queue, Process
import time
import logging

logging.basicConfig(format='%(levelname)s:%(name)s:%(funcName)s: %(message)s' ,level=logging.INFO)
logger = logging.getLogger(__name__)

def is_goal_reached(goal_point, robot_cell, distance_to_trigger_goal_m, size_of_cell_in_meter):
    """
    Tells if the goal has been reached or not.
    :param goal_point: The goal point.
    :type goal_point: Position
    :param robot_cell: The robot position in the grid.
    :type robot_cell: Position
    :param distance_to_trigger_goal_m: Distance under which the robot triggers the goal, in meters.
    :type distance_to_trigger_goal_m: float
    :param size_of_cell_in_meter: Size of a cell of the grid in meters.
    :type size_of_cell_in_meter: float
    :return: True if the goal is reached, False otherwise.
    :rtype: boolean
    """
    if goal_point != None:
        dist_2 = distance_2(robot_cell, goal_point)
        trigger_2 = (distance_to_trigger_goal_m * (1.0 / size_of_cell_in_meter))**2
        goal_reached = (dist_2 <= trigger_2)
        if goal_reached:
            logger.info('Goal reached')
        return goal_reached
    return False

def cartographer_job(queue_cartographer, queue_show_map, robot_map, robot):
    cartographer = Cartographer()
    while True:
        robot_pos = robot.position
        robot_lasers = robot.lasers
        robot_map = cartographer.update(robot_map, robot_pos, robot_lasers)
        queue_cartographer.put(robot_map)
        queue_sm_map.put(robot_map)
        time.sleep(0.1)

def show_map_job(queue_sm_map, queue_sm_optionals, robot_map, robot):
    show_map = ShowMap(robot_map.grid)
    frontiers = None
    forces = None
    goal_point = None
    while True:
        while not queue_sm_map.empty():
            robot_map = queue_show_map.get()
        while not queue_sm_optionals.empty():
            frontiers, forces, goal_point = queue_sm_optionals.get()
        robot_pos = robot.position
        robot_cell = robot_map.to_grid_pos(robot_pos)
        show_map.update(robot_map, robot_cell, frontiers=frontiers, goal_point=goal_point, forces=forces)
        time.sleep(0.1)

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
    controller = Controller(robot)
    potential_field = PotentialField(robot)
    goal_planner = GoalPlanner()

    queue_cartographer = Queue()
    queue_sm_map = Queue()
    queue_sm_optionals = Queue()

    cartographer_process = Process(target=cartographer_job, args=(queue_cartographer, queue_show_map, robot_map, robot))
    cartographer_process.daemon = True
    cartographer_process.start()

    show_map_process = Process(target=show_map_job, args=(queue_sm_map, queue_sm_optionals, robot_map, robot))
    show_map_process.daemon = True
    show_map_process.start()

    #show_map = ShowMap(robot_map.grid)

    frontiers = None
    goal_point = None
    start = time.time()
    delay = 10

    controller.turn_around()
    while True:
        #Communicate with the cartographer
        while not queue_cartographer.empty():
            robot_map = queue_cartographer.get()
        #Rest of the program
        robot_pos = robot.position
        robot_cell = robot_map.to_grid_pos(robot_pos)
        forces = potential_field.get_forces(robot_cell, goal_point, robot_map)
        controller.apply_force(forces['gen_force'], robot_pos)
        goal_reached = is_goal_reached(goal_point, robot_cell, distance_to_trigger_goal_m, size_of_cell_in_meter)
        if time.time() - start >= delay or goal_reached:
            controller.stop()
            goal_point, frontiers = goal_planner.get_goal_point(robot_cell, robot_map)
            start = time.time()
            delay = 20
        #Communicate with show_map
        queue_sm_optionals.put([frontiers, forces, goal_point])
        #show_map.update(robot_map, robot_cell, frontiers=frontiers, goal_point=goal_point, forces=forces)
    cartographer_process.terminate()
