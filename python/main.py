from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from utils.position import Position
import time

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter

    robot = Robot(url)
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    cartographer = Cartographer(robot_map)
    show_map = ShowMap(robot_map)

    #while True:
    for _ in range(25):
        robot_pos = robot.position
        robot_lasers = robot.lasers
        cartographer.update(robot_pos, robot_lasers)
        show_map.update(robot_map.to_grid_pos(robot_pos))

    print('Stop the robot')
    time.sleep(2)

    frontiers = robot_map.get_divided_frontiers()
    show_map.update(robot_map.to_grid_pos(robot.position), frontiers=frontiers)
