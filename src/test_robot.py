from robot import Robot
from math import cos, sin
import time

url = 'localhost:50000'

robot = Robot(url)
robot.post_speed(0.3, 0.3)

while True:
    robot_pos = robot.position
    lasers = robot.lasers
    print(robot_pos)
    distance_to_laser = 0.15
    laser_pos_x = robot_pos.x + distance_to_laser * cos(robot_pos.angle)
    laser_pos_y = robot_pos.y + distance_to_laser * sin(robot_pos.angle)
    print('Laser pos: x: ' + str(laser_pos_x) + ' y: ' + str(laser_pos_y))
    for laser in lasers:
        angle = robot_pos.angle + laser.angle
        laser_hit_x = laser_pos_x + laser.echoe * cos(angle)
        laser_hit_y = laser_pos_y + laser.echoe * sin(angle)
        print('Laser hit: x: ' + str(laser_hit_x) + ' y: ' + str(laser_hit_y))
    print('\n\n\n\n')
    time.sleep(5)
