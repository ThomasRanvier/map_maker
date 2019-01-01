from logging import getLogger
from math import hypot, atan, cos, sin

logger = getLogger('controller')

class Controller:
    def __init__(self, robot, robot_map):
        self.__map = robot_map
        self.__robot = robot
    
    def go_to_goal_point(self, robot_cell, goal_point):
        if goal_point == None:
            return
        pass

    def attractive_force(self, robot_cell, goal_point):
        if goal_point == None:
            return None
        length = 0.2 * hypot(robot_cell.x - goal_point.x, robot_cell.y - goal_point.x)
        dx = goal_point.x - robot_cell.x
        dy = goal_point.y - robot_cell.y
        angle = atan(dy / dx)
        logger.info('dx: ' + str(dx))
        logger.info('dy: ' + str(dy))
        logger.info('Angle: ' + str(angle))
        targetx = length * cos(angle)
        targety = length * sin(angle)
        logger.info('tx: ' + str(targetx))
        logger.info('ty: ' + str(targety))
        return {'x': robot_cell.x, 'y': robot_cell.y, 'targetx': length * cos(angle), 'targety': length * sin(angle)}

    def turn_around(self):
        logger.info('Make the robot turn around')
        self.__robot.post_speed(1, 1)

    def stop(self):
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
