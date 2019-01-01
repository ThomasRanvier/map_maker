from logging import getLogger

logger = getLogger('controller')

class Controller:
    def __init__(self, robot):
        self.__robot = robot
    
    def apply_force(self, force, robot_pos):
        pass

    def turn_around(self):
        logger.info('Make the robot turn around')
        self.__robot.post_speed(1, 1)

    def stop(self):
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
