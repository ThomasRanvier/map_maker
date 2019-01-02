import http.client, json
from utils.position import Position
from utils.laser import Laser
from utils.utils import orientation_to_angle
from math import pi
from logging import getLogger
import time

logger = getLogger('robot')

class Robot:
    """
    Class that implements a Robot, it is used as an interface to communicate directly with the MRDS server.
    """

    def __init__(self, url, min_delay = 0.05):
        """
        Instantiates a Robot.
        :param url: The url of the MRDS server.
        :type url: string
        """
        self.__url = url
        self.HEADERS = {"Content-type": "application/json", "Accept": "text/json"}
        self.__min_delay = min_delay
        self.__timer_position = 0
        self.__timer_lasers = 0
        self.__last_position = None
        self.__last_lasers = None

    def post_speed(self, angular_speed, linear_speed):
        """
        Post the angular and linear speeds to the MRDS server, it will apply them to the robot.
        :param angular_speed: The angular speed to apply.
        :type angular_speed: float
        :param linear_speed: The linear speed to apply.
        :type linear_speed: float
        :return: The response of the request.
        :rtype: response
        """
        params = json.dumps({'TargetAngularSpeed': angular_speed, 'TargetLinearSpeed': linear_speed})
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('POST', '/lokarria/differentialdrive', params, self.HEADERS)
        response = mrds.getresponse()
        status = response.status
        if status == 204:
            logger.info('Update robot speed')
            return response
        else:
            logger.info('Impossible to post robot speed')
            return None

    @property
    def position(self):
        """
        Requests the position of the robot and gives it in a Position object.
        :return: The position of the robot.
        :rtype: Position 
        """
        if time.time() - self.__timer_position < self.__min_delay:
            return self.__last_position
        self.__timer_position = time.time()
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('GET', '/lokarria/localization')
        response = mrds.getresponse()
        if (response.status == 200):
            pose_data = response.read()
            response.close()
            pos = json.loads(pose_data.decode())['Pose']
            self.__last_position = Position(pos['Position']['X'], pos['Position']['Y'], pos['Position']['Z'], orientation_to_angle(pos['Orientation']))
            return self.__last_position
        else:
            logger.info('Impossible to get the robot pose')
            return None

    @property
    def lasers(self):
        """
        Requests the lasers responses and gives a list of Laser objects.
        :return: The lasers results.
        :rtype: A list of Laser objects.
        """
        if time.time() - self.__timer_lasers < self.__min_delay:
            return self.__last_lasers
        self.__timer_lasers = time.time()
        laser_echoes = self.__get_laser_echoes()
        laser_angles = self.__get_laser_angles()
        if laser_echoes != None and laser_angles != None:
            lasers = []
            for i in range(len(laser_echoes)):
                lasers.append(Laser(laser_echoes[i], laser_angles[i]))
            self.__last_lasers = lasers
            return self.__last_lasers
        else:
            logger.info('Impossible to get the robot lasers')
            return None

    def __get_laser_echoes(self):
        """
        Requests the lasers echoes.
        :return: The lasers echoes.
        :rtype: Lasers echoes.
        """
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('GET', '/lokarria/laser/echoes')
        response = mrds.getresponse()
        if response.status == 200:
            laser_data = response.read().decode('utf-8')
            response.close()
            laser_scan = json.loads(laser_data)
            return laser_scan['Echoes']
        else:
            logger.info('Impossible to get the robot laser echoes')
            return None

    def __get_laser_angles(self):
        """
        Requests the lasers angles.
        :return: The lasers angles.
        :rtype: Lasers angles.
        """
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('GET', '/lokarria/laser/properties')
        response = mrds.getresponse()
        if response.status == 200:
            laser_data = response.read().decode('utf-8')
            response.close()
            properties = json.loads(laser_data)
            a = properties['StartAngle']
            angles = []
            while a <= properties['EndAngle']:
                angles.append(a)
                a += pi / 180
            return angles
        else:
            logger.info('Impossible to get the robot laser angles')
            return None
