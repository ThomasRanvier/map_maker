from mapping.show_map import ShowMap
from mapping.map import Map
from utils.position import Position
from planning.goal_planner import GoalPlanner
import time

robot_pos = Position(9, 9)
lower_left_pos = Position(-5.0, -5.0)
upper_right_pos = Position(5.0, 5.0)
test_map = Map(lower_left_pos, upper_right_pos, 1.0)
goal_planner = GoalPlanner(test_map, 0)
show_map = ShowMap(test_map, True)

for x in range(test_map.grid_width):
    for y in range(test_map.grid_height):
        test_map.grid[x][y] = 0

for x in range(2):
    for y in range(test_map.grid_height):
        test_map.grid[x][y] = 0.5

for x in range(test_map.grid_height):
    for y in range(2):
        test_map.grid[x][y] = 0.5

for y in range(7, 8):
    test_map.grid[2][y] = 1

for y in range(4, 6):
    test_map.grid[2][y] = 1

for x in range(6, 9):
    test_map.grid[x][2] = 1

divided_frontiers = goal_planner.get_frontiers(test_map.to_real_pos(robot_pos))
if divided_frontiers:
    for frontier in divided_frontiers:
        print('-----New frontier-----')
        for cell in frontier:
            print(cell)

while True:
    show_map.update(robot_pos, frontiers=divided_frontiers)
    time.sleep(0.1)
