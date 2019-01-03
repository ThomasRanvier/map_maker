import time
from mapping.cartographer import Cartographer
from mapping.show_map import ShowMap
from logging import getLogger
from utils.utils import filled_midpoint_circle

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
    goal_point = None
    while True:
        start = time.time()
        while not queue_sm_map.empty():
            robot_map = queue_sm_map.get()
        while not queue_sm_optionals.empty():
            frontiers, forces, goal_point = queue_sm_optionals.get()
        robot_pos = robot.position
        robot_cell = robot_map.to_grid_pos(robot_pos)
        show_map.update(robot_map, robot_cell, frontiers=frontiers, goal_point=goal_point, forces=forces)
        sleep = 0.5 - (time.time() - start)
        if sleep > 0:
            time.sleep(sleep)

def frontiers_limiter_job(queue_fl_closest_frontier, queue_fl_ignored_cells, queue_fl_stuck, robot_map, robot, max_positions = 20, delta_m = 5, radius = 6):
    """
    This is the job that tells to the goal planner all the cells to ignore when it is building the frontiers.
    It detects when the robot is stuck and then adds all the cells around the closest frontier in a radius of 'radius' and sends that updated list to the goal planner.
    :param queue_fl_closest_frontier: The queue where the goal planner puts the closest frontier.
    :type queue_fl_closest_frontier: Queue
    :param queue_fl_ignored_cells: The queue where this job puts the updated list of cells to ignore.
    :type queue_fl_ignored_cells: Queue
    :param queue_fl_stuck: The queue where this job puts True if the robot is stuck, used by main to request new search of frontiers
    :type queue_fl_stuck: Queue
    :param robot_map: The map.
    :type robot_map: Map
    :param robot: The robot to request the position.
    :type robot: Robot
    :param max_positions: The number of positions to memorise before analysing the deltas.
    :type max_positions: integer
    :param delta_m: The delta in meter bellow which the robot is detected as stuck.
    :type delta_m: float
    :param radius: The radius (in cells of the grid) around the closest frontier in which the cells are added to the ignored cells set.
    :type radius: integer
    """
    last_positions = []
    ignored_cells = set([])
    closest_frontier = None
    stuck_count = 0
    while True:
        stuck = False
        while not queue_fl_closest_frontier.empty():
            closest_frontier = queue_fl_closest_frontier.get()
        if closest_frontier != None:
            robot_pos = robot.position
            last_positions.append(robot_pos)
            if len(last_positions) > max_positions:
                last_positions.pop(0)
                min_x = last_positions[0].x
                max_x = min_x
                min_y = last_positions[0].y
                max_y = min_y
                for pos in last_positions:
                    if min_x > pos.x:
                        min_x = pos.x
                    if min_y > pos.y:
                        min_y = pos.y
                    if max_x < pos.x:
                        max_x = pos.x
                    if max_y < pos.y:
                        max_y = pos.y
                delta_x = abs(max_x - min_x)
                delta_y = abs(max_y - min_y)
                if delta_x <= delta_m + 2 and delta_y <= delta_y + 2:
                    logger.info('Delta x: ' + str(delta_x))
                    logger.info('Delta y: ' + str(delta_y))
                if delta_x <= delta_m and delta_y <= delta_m:
                    last_positions = []
                    stuck = True
                    stuck_count += 1
                    if stuck_count == 2:
                        logger.info('Robot is detected as stuck twice in a row, delete closest_frontier')
                        for p in closest_frontier:
                            for n in filled_midpoint_circle(p.x, p.y, radius):
                                if robot_map.is_in_bound(n):
                                    ignored_cells.add(n)
                        stuck = False
                        stuck_count = 0
                    else:
                        logger.info('Robot is detected as stuck, go to biggest frontier')
                else:
                    stuck_count = 0
        while not queue_fl_ignored_cells.empty():
            queue_fl_ignored_cells.get()
        queue_fl_ignored_cells.put(ignored_cells)
        if stuck:
            queue_fl_stuck.put(True)
        time.sleep(1)
