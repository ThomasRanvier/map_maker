from mapping.show_map import ShowMap
from mapping.map import Map
from utils.position import Position
import time

robot_pos = Position(0, 0)
lower_left_pos = Position(-5.0, -5.0)
upper_right_pos = Position(5.0, 5.0)
test_map = Map(lower_left_pos, upper_right_pos, 2.0)
show_map = ShowMap(test_map, True)

test_map.grid[0][0] = 0
test_map.grid[1][0] = 0
test_map.grid[2][0] = 0
test_map.grid[1][1] = 0
test_map.grid[2][1] = 0
test_map.grid[2][2] = 0
test_map.grid[1][2] = 0

test_map.grid[5][5] = 1
test_map.grid[5][6] = 1
test_map.grid[5][7] = 1
test_map.grid[6][5] = 1
test_map.grid[6][7] = 1
test_map.grid[7][6] = 1
test_map.grid[7][7] = 1

test_map.grid[19][19] = 1

while True:
    show_map.update(robot_pos)
    if robot_pos.x < test_map.grid_width - 1:
        robot_pos.x += 1
    elif robot_pos.y < test_map.grid_height - 1:
        robot_pos.y += 1
    time.sleep(0.1)
