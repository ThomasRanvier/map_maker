import http.client, json
from utils.position import Position
from utils.laser import Laser
from utils.utils import orientation_to_angle
from math import pi

class Robot:
    def __init__(url):
        self.__url = url

    def post_speed(self, angular_speed, linear_speed):
        params = json.dumps({'TargetAngularSpeed': angular_speed, 'TargetLinearSpeed': linear_speed})
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
        response = mrds.getresponse()
        status = response.status
        response.close()
        if status == 204:
            return response
        else:
            print('Impossible to post robot speed')
            return None

    @property
    def position(self):
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('GET', '/lokarria/localization')
        response = mrds.getresponse()
        if (response.status == 200):
            pose_data = response.read()
            response.close()
            pos = json.loads(pose_data.decode())
            return Position(pos['Pose']['X'], pos['Pose']['Y'], pos['Pose']['Z'], orientation_to_angle(pos['Orientation']))
        else:
            print('Impossible to get the robot pose')
            return None

    @property
    def lasers(self):
        laser_echoes = self.__get_laser_echoes()
        laser_angles = self.__get_laser_angles()
        if laser_echoes != None and laser_angles != None:
            lasers = []
            for i in range(len(laser_echoes)):
                lasers.append(Laser(laser_echoes[i], laser_angles[i]))
            return lasers
        else:
            print('Impossible to get the robot lasers')
            return None

    def __get_laser_echoes(self):
        mrds = http.client.HTTPConnection(self.__url)
        mrds.request('GET', '/lokarria/laser/echoes')
        response = mrds.getresponse()
        if response.status == 200:
            laser_data = response.read().decode('utf-8')
            response.close()
            laser_scan = json.loads(laser_data)
            return laser_scan['Echoes']
        else:
            print('Impossible to get the robot laser echoes')
            return None

    def __get_laser_angles(self):
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
            print('Impossible to get the robot laser angles')
            return None

