from robot import Robot
from mapping.cartographer import Cartographer
from mapping.map import Map
from mapping.show_map import ShowMap
from utils.position import Position

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

    while True:
        cartographer.update(robot.position, robot.lasers)
        show_map.update(robot_map.to_grid_pos(robot.position))
