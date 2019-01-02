import time
from mapping.cartographer import Cartographer
from mapping.show_map import ShowMap

def cartographer_job(queue_cartographer, queue_sm_map, robot_map, robot):
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
        sleep = 0.2 - (time.time() - start)
        if sleep > 0:
            time.sleep(sleep)
