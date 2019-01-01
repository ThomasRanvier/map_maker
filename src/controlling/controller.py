from logging import getLogger

logger = getLogger('controller')

class Controller:
    def __init__(self, robot, robot_map):
        self.__map = robot_map
        self.__robot = robot
    
    def go_to_goal_point(self, goal_point):
        if goal_point == None:
            return
        pass

    def turn_around(self):
        logger.info('Make the robot turn around')
        self.__robot.post_speed(1, 1)

    def stop(self):
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
