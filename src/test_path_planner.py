from mapping.show_map import ShowMap
from mapping.map import Map
from utils.position import Position
from planning.goal_planner import GoalPlanner
from planning.path_planner import PathPlanner
from multiprocessing import Queue
import time
import logging
from math import hypot

logging.basicConfig(format='%(levelname)s:%(name)s:%(funcName)s: %(message)s' ,level=logging.INFO)
logger = logging.getLogger(__name__)

def has_progressed(path, robot_cell, distance_to_trigger_goal):
    """
    Tells if the robot has progressed on the path or not.
    :param path: The path to follow.
    :type path: A list of Position objects.
    :param robot_cell: The position of the robot in the grid.
    :type robot_cell: Position
    :param distance_to_trigger_goal: Distance under which the robot triggers the goal.
    :type distance_to_trigger_goal: float
    """
    if path != []:
        dist = hypot(path[0].x - robot_cell.x, path[0].y - robot_cell.y)
        has_progressed = (dist <= distance_to_trigger_goal)
        if has_progressed:
            path.pop(0)
            logger.info('Has progressed')
            if path == []:
                logger.info('Has finished')
        return (has_progressed, path == [])
    return (False, False)

robot_cell = Position(300, 300)
lower_left_pos = Position(-100.0, -100.0)
upper_right_pos = Position(100.0, 100.0)
test_map = Map(lower_left_pos, upper_right_pos, 2)
path_planner = PathPlanner(3 * 2, 8 * 2)
show_map = ShowMap(test_map.grid, True)

for x in range(test_map.grid_width):
    for y in range(test_map.grid_height):
        test_map.grid[x][y] = 0

for x in range(0, 250):
    for y in range(0, 250):
        test_map.grid[x][y] = 1
goal_point = Position(298, 298)
start = time.time()
path = path_planner.get_path(robot_cell, test_map, goal_point)
print(time.time() - start)

while True:
    show_map.update(test_map, robot_cell, path=path)
    robot_cell.x -= 1
    robot_cell.y -= 1
    progressed, finished = has_progressed(path, robot_cell, 3 * 2)
    time.sleep(0.05)
