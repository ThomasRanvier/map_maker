from logging import getLogger

logger = getLogger('controller')

class Controller:
    """
    Class that implements a Controller, used as an interface to communicate easily with the Robot object which communicates directly with the MRDS server.
    """

    def __init__(self, robot):
        """
        Instantiates a Controller.
        :param robot: The robot to interface.
        :type robot: Robot
        """
        self.__robot = robot
    
    def apply_force(self, force, robot_pos):
        """
        Applies the force to the robot, converts the force into commands to send to the robot.
        :param force: The force to apply.
        :type force: Dictionary of the coordinates of the force vector.
        :param robot_pos: The position of the robot in the real world.
        :type robot_pos: Position
        """
        #Convert force vector in angle and length
        pass

    def turn_around(self):
        """
        Makes the robot turn in circles, slow enough to have a precise lasers reading.
        """
        logger.info('Make the robot turn around')
        self.__robot.post_speed(0.75, 0.5)

    def stop(self):
        """
        Makes the robot stop moving.
        """
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
