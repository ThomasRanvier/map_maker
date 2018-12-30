from robot import Robot
from mapping.mapper import Mapper
from mapping.map import Map
from mapping.show_map import ShowMap
from utils.position import Position

if __name__ == '__main__':
    url = 'localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter
    laser_max_distance = 0.15

    robot = Robot(url)
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)
    robot_map = Map(lower_left_pos, upper_right_pos, scale)
    mapper = Mapper(robot_map, laser_max_distance)
    show_map = ShowMap(robot_map)

    while True:
        mapper.udpate(robot.position, robot.lasers)
        show_map.udpate(robot.position)
