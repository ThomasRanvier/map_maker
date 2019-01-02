import time
from mapping.cartographer import Cartographer
from mapping.show_map import ShowMap

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
