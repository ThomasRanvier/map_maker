from robot import Robot
from mapper import Mapper, Map

if __name__ == '__main__':
    url = 'http://localhost:50000'
    size_of_cell_in_meter = 0.5
    scale = 1 / size_of_cell_in_meter

    robot = Robot(url)
    lower_left_pos = Position(-100.0, -100.0)
    upper_right_pos = Position(100.0, 100.0)
    mapper = Mapper(Map(lower_left_pos, upper_right_pos, scale))

    while True:
        mapper.udpate(robot.pose, robot.lasers)
