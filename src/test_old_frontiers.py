from mapping.show_map import ShowMap
from mapping.map import Map
from utils.position import Position
import time

"""
Test of the old way of finding the frontiers, to run it paste the following code in map.py.

def __get_frontiers(self):
    frontiers = []
    for x in range(self.grid_width):
        for y in range(self.grid_height):
            cell = Position(x, y)
            if self.is_unknown(cell):
                for neighbour in von_neumann_neighbourhood(cell, self.grid_width, self.grid_height):
                    if neighbour not in frontiers and self.is_empty(neighbour):
                        frontiers.append(neighbour)
    return frontiers

def __build_frontier(self, frontiers, current_frontier, cell):
    neighbours = moore_neighbourhood(cell, self.grid_width, self.grid_height)
    for neighbour in neighbours:
        if neighbour in frontiers:
            current_frontier.append(neighbour)
            frontiers.remove(neighbour)
            self.__build_frontier(frontiers, current_frontier, neighbour)

def get_divided_frontiers(self):
    frontiers = self.__get_frontiers()
    divided_frontiers = [frontiers]
    while frontiers:
        current_frontier = []
        cell = frontiers.pop(0)
        current_frontier.append(cell)
        self.__build_frontier(frontiers, current_frontier, cell)
        divided_frontiers.append(current_frontier)
    return divided_frontiers
"""

robot_pos = Position(9, 9)
lower_left_pos = Position(-5.0, -5.0)
upper_right_pos = Position(5.0, 5.0)
test_map = Map(lower_left_pos, upper_right_pos, 1.0)
show_map = ShowMap(test_map.grid, True)

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

divided_frontiers = test_map.get_divided_frontiers()
if divided_frontiers:
    for frontier in divided_frontiers:
        print('-----New frontier-----')
        for cell in frontier:
            print(cell)

while True:
    show_map.update(test_map, robot_pos, frontiers=divided_frontiers)
    time.sleep(0.1)
