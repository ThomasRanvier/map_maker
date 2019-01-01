from controlling.controller import Controller
from robot import Robot
from mapping.map import Map
from utils.position import Position
import json, http.client
from logging

"""
robot = Robot('localhost:50000')
size_of_cell_in_meter = 0.5
scale = 1 / size_of_cell_in_meter
lower_left_pos = Position(-100.0, -100.0)
upper_right_pos = Position(100.0, 100.0)
robot_map = Map(lower_left_pos, upper_right_pos, scale)
controller = Controller(robot, robot_map)
controller.turn_around()
"""
logging.basicConfig(format='%(levelname)s:%(name)s:%(funcName)s: %(message)s' ,level=logging.INFO)
logger = logging.getLogger('test controller')

HEADERS = {"Content-type": "application/json", "Accept": "text/json"}
params = json.dumps({'TargetAngularSpeed': 2, 'TargetLinearSpeed': 2})
mrds = http.client.HTTPConnection('localhost:50000')
mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
response = mrds.getresponse()
status = response.status
if status == 204:
    logger.info('Ok')
else:
    logger.info('Impossible to post robot speed')

while True:
    pass
