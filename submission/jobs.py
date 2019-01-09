import time
import sys
from cartographer import Cartographer
from show_map import ShowMap
from logging import getLogger
from utils import filled_midpoint_circle, get_deltas

logger = getLogger('jobs')

def cartographer_job(queue_cartographer, queue_sm_map, robot_map, robot):
    """
    Cartographer's job, used to make the cartographer run on the back ground and so the update of the map is not slowed down by anything.
    :param queue_cartographer: The queue used to communicate with the main process, this subprocess puts the last updated version of the map in the queue at any update.
    :type queue_cartographer: Queue
    :param queue_sm_map: The queue used to communicate with the show map process, this subprocess puts the last updated version of the map in the queue at any update.
    :type queue_sm_map: Queue
    :param robot_map: The map to update.
    :type robot_map: Map
    :param robot: The Robot object used to communicate with the MRDS server.
    :type robot: Robot
    """
    cartographer = Cartographer()
    while True:
        start = time.time()
        robot_pos = robot.position
        robot_lasers = robot.lasers
        robot_map = cartographer.update(robot_map, robot_pos, robot_lasers)
        queue_cartographer.put(robot_map)
        queue_sm_map.put(robot_map)
        sleep = 0.1 - (time.time() - start)
        if sleep > 0:
            time.sleep(sleep)

def show_map_job(queue_sm_map, queue_sm_optionals, robot_map, robot):
    """
    ShowMap's job, used to display the map with useful informations to the screen.
    Slow process so being in a subprocess saves a lot of time.
    :param queue_sm_map: The queue used where the cartographer process sends the last updated version of the map in the queue at any update.
    :type queue_sm_map: Queue
    :param queue_sm_optionals: The queue where the main process sends the optional options that the ShowMap can display: frontiers, goal and forces.
    :type queue_sm_optionals: Queue
    :param robot_map: The map to display.
    :type robot_map: Map
    :param robot: The robot used to communicate with the MRDS server.
    :type robot: Robot
    """
    show_map = ShowMap(robot_map.grid)
    frontiers = None
    forces = None
    path = None
    while True:
        start = time.time()
        while not queue_sm_map.empty():
            robot_map = queue_sm_map.get()
        while not queue_sm_optionals.empty():
            frontiers, forces, path = queue_sm_optionals.get()
        robot_pos = robot.position
        robot_cell = robot_map.to_grid_pos(robot_pos)
        show_map.update(robot_map, robot_cell, frontiers=frontiers, path=path, forces=forces)
        sleep = 0.5 - (time.time() - start)
        if sleep > 0:
            time.sleep(sleep)

def frontiers_limiter_job(queue_fl_current_frontier, queue_fl_ignored_cells, robot, max_positions_immobile = 5, max_positions_stuck = 20, delta_m_immobile = 0.2, delta_m_stuck = 3.5, radius = 6):
    """
    This is the job that tells to the goal planner all the cells to ignore when it is building the frontiers.
    It detects when the robot is stuck and then adds all the cells around the current frontier in a radius of 'radius' and sends that updated list to the goal planner.
    :param queue_fl_current_frontier: The queue where the goal planner puts the current frontier.
    :type queue_fl_current_frontier: Queue
    :param queue_fl_ignored_cells: The queue where this job puts the updated list of cells to ignore.
    :type queue_fl_ignored_cells: Queue
    :param robot: The robot to request the position.
    :type robot: Robot
    :param max_positions_immobile: The number of positions to memorise before analysing the deltas to detect if the robot is immobile.
    :type max_positions_immobile: A list of Position objects.
    :param max_positions_stuck: The number of positions to memorise before analysing the deltas to detect if the robot is stuck.
    :type max_positions_stuck: A list of Position objects.
    :param delta_m_immobile: The delta in meter below which the robot is detected as immobile.
    :type delta_m_immobile: float
    :param delta_m_stuck: The delta in meter below which the robot is detected as stuck.
    :type delta_m_stuck: float
    :param radius: The radius (in cells of the grid) around the current frontier in which the cells are added to the ignored cells set.
    :type radius: integer
    """
    def delete_frontier(frontier, ignored_cells):
        """
        The function used to delete the frontier when the robot is either detected as stuck or immobile.
        :param frontier: The frontier.
        :type frontier: A list of Position objects.
        :param ignored_cells: The list of cells to ignore for the goal planner.
        :type ignored_cells: A list of Position objects.
        """
        for p in frontier:
            for n in filled_midpoint_circle(p.x, p.y, radius):
                ignored_cells.add(n)

    last_positions = []
    ignored_cells = set([])
    current_frontier = None
    while True:
        while not queue_fl_current_frontier.empty():
            current_frontier = queue_fl_current_frontier.get()
        if current_frontier != None:
            robot_pos = robot.position
            last_positions.append(robot_pos)
            immobile = False
            if len(last_positions) >= max_positions_immobile:
                delta_x, delta_y = get_deltas(last_positions, max_positions_immobile)
                if delta_x <= delta_m_immobile and delta_y <= delta_m_immobile:
                    last_positions = []
                    immobile = True
                    logger.info('Robot is detected as immobile, delete current frontier')
                    delete_frontier(current_frontier, ignored_cells)
            if not immobile and len(last_positions) > max_positions_stuck:
                last_positions.pop(0)
                delta_x, delta_y = get_deltas(last_positions, max_positions_stuck)
                if delta_x <= delta_m_stuck + 1 and delta_y <= delta_m_stuck + 1:
                    logger.info('Delta x: ' + str(delta_x) + ', delta y: ' + str(delta_y))
                if delta_x <= delta_m_stuck and delta_y <= delta_m_stuck:
                    last_positions = []
                    logger.info('Robot is detected as stuck, delete current frontier')
                    delete_frontier(current_frontier, ignored_cells)
        queue_fl_ignored_cells.put(ignored_cells)
        time.sleep(1)
