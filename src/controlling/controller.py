from logging import getLogger
from math import hypot, atan2, sin, log10
import time

logger = getLogger('controller')

class Controller:
    """
    Class that implements a Controller, used as an interface to communicate easily with the Robot object which communicates directly with the MRDS server.
    """

    def __init__(self, robot, max_ang_speed = 3, ang_speed_weight = 0.8, turn_around_delay = 8):
        """
        Instantiates a Controller.
        :param robot: The robot to interface.
        :type robot: Robot
        :param max_ang_speed: The robot max angular speed.
        :type max_ang_speed: float
        :param ang_speed_weight: The weight to apply to the angular speed.
        :type ang_speed_weight: float
        :param turn_around_delay: The delay applied between the action of turning around and the action of applying the forces to the robot.
        :type turn_around_delay: float
        """
        self.__robot = robot
        self.__max_ang_speed = max_ang_speed
        self.__ang_speed_weight = ang_speed_weight
        self.__timer = 0
        self.__turn_around_delay = turn_around_delay
    
    def apply_force(self, force, robot_pos):
        """
        Applies the force to the robot, converts the force into commands to send to the robot.
        :param force: The force to apply.
        :type force: Dictionary of the coordinates of the force vector.
        :param robot_pos: The position of the robot in the real world.
        :type robot_pos: Position
        """
        if time.time() - self.__timer < self.__turn_around_delay:
            return
        elif force['x'] == 0 and force['y'] == 0:
            self.stop()
        else:
            force_length = hypot(force['x'], force['y'])
            force_angle = atan2(force['y'], force['x'])
            theta = sin(force_angle - robot_pos.angle)
            ang_speed = self.__max_ang_speed * theta * self.__ang_speed_weight
            ang_speed = min(max(ang_speed, -self.__max_ang_speed), self.__max_ang_speed)
            self.__robot.post_speed(ang_speed, max(0, 0.5 + log10(-ang_speed + (self.__max_ang_speed - 0.5))))

    def turn_around(self):
        """
        Makes the robot turn in circles, slow enough to have a precise lasers reading, overrules the timer.
        """
        self.__timer = time.time()
        logger.info('Make the robot turn around')
        self.__robot.post_speed(0.75, 0.5)

    def stop(self):
        """
        Makes the robot stop moving, overrules the timer.
        """
        logger.info('Stop the robot')
        self.__robot.post_speed(0, 0)
