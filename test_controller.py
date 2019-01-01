from controlling.controller import Controller
from robot import Robot
from mapping.map import Map

robot = Robot('localhost:50000')
size_of_cell_in_meter = 0.5
scale = 1 / size_of_cell_in_meter
lower_left_pos = Position(-100.0, -100.0)
upper_right_pos = Position(100.0, 100.0)
robot_map = Map(lower_left_pos, upper_right_pos, scale)
controller = Controller(robot, robot_map)
controller.post_speed(2, 2)

while True:
    pass
