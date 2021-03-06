from mapping.map import Map
from utils.position import Position
from utils.utils import bresenham_line, filled_midpoint_circle
import matplotlib.pyplot as plt

def map_to_grid_pos():
    print('Test: map_to_grid_pos')
    lower_left_pos = Position(-5.0, -5.0)
    upper_right_pos = Position(5.0, 5.0)
    test_map = Map(lower_left_pos, upper_right_pos, 2.0)
    assert(test_map.grid.shape == (20, 20))
    grid_pos = test_map.to_grid_pos(Position(-5, -5))
    assert(grid_pos.x == 0 and grid_pos.y == 0)
    grid_pos = test_map.to_grid_pos(Position(-4.5, -5))
    assert(grid_pos.x == 1 and grid_pos.y == 0)
    grid_pos = test_map.to_grid_pos(Position(-4.501, -5))
    assert(grid_pos.x == 0 and grid_pos.y == 0)
    grid_pos = test_map.to_grid_pos(Position(5, 5))
    assert(grid_pos.x == 20 and grid_pos.y == 20)
    grid_pos = test_map.to_grid_pos(Position(4.99, 4.99))
    assert(grid_pos.x == 19 and grid_pos.y == 19)
    print('OK')

def map_to_real_pos():
    print('Test: map_to_real_pos')
    lower_left_pos = Position(-5.0, -5.0)
    upper_right_pos = Position(5.0, 5.0)
    test_map = Map(lower_left_pos, upper_right_pos, 2.0)
    assert(test_map.grid.shape == (20, 20))
    real_pos = test_map.to_real_pos(Position(0, 0))
    assert(real_pos.x == -5 and real_pos.y == -5)
    real_pos = test_map.to_real_pos(Position(1, 0))
    assert(real_pos.x == -4.5 and real_pos.y == -5)
    real_pos = test_map.to_real_pos(Position(2, 0))
    assert(real_pos.x == -4 and real_pos.y == -5)
    real_pos = test_map.to_real_pos(Position(20, 20))
    assert(real_pos.x == 5 and real_pos.y == 5)
    real_pos = test_map.to_real_pos(Position(19, 19))
    assert(real_pos.x == 4.5 and real_pos.y == 4.5)
    print('OK')

def utils_bresenham_line():
    print('Test: utils_bresenham_line')
    line = bresenham_line(0, 0, 5, 5)
    assert(line[0].x == 0 and line[0].y == 0)
    assert(line[1].x == 1 and line[1].y == 1)
    assert(line[2].x == 2 and line[2].y == 2)
    assert(line[3].x == 3 and line[3].y == 3)
    assert(line[4].x == 4 and line[4].y == 4)
    assert(line[5].x == 5 and line[5].y == 5)
    line = bresenham_line(5, 5, 0, 0)
    assert(line[0].x == 5 and line[0].y == 5)
    assert(line[1].x == 4 and line[1].y == 4)
    assert(line[2].x == 3 and line[2].y == 3)
    assert(line[3].x == 2 and line[3].y == 2)
    assert(line[4].x == 1 and line[4].y == 1)
    assert(line[5].x == 0 and line[5].y == 0)
    line = bresenham_line(2, 5, 8, 9)
    assert(line[0].x == 2 and line[0].y == 5)
    assert(line[1].x == 3 and line[1].y == 6)
    assert(line[2].x == 4 and line[2].y == 6)
    assert(line[3].x == 5 and line[3].y == 7)
    assert(line[4].x == 6 and line[4].y == 8)
    assert(line[5].x == 7 and line[5].y == 8)
    assert(line[6].x == 8 and line[6].y == 9)
    print('OK')

def utils_filled_midpoint_circle():
    print('Test: utils_filled_midpoint_circle')
    circle = filled_midpoint_circle(5, 5, 5)
    result = [' x: 0 y: 5',
                ' x: 1 y: 5',
                ' x: 2 y: 5',
                ' x: 3 y: 5',
                ' x: 4 y: 5',
                ' x: 5 y: 5',
                ' x: 6 y: 5',
                ' x: 7 y: 5',
                ' x: 8 y: 5',
                ' x: 9 y: 5',
                ' x: 10 y: 5',
                ' x: 0 y: 6',
                ' x: 1 y: 6',
                ' x: 2 y: 6',
                ' x: 3 y: 6',
                ' x: 4 y: 6',
                ' x: 5 y: 6',
                ' x: 6 y: 6',
                ' x: 7 y: 6',
                ' x: 8 y: 6',
                ' x: 9 y: 6',
                ' x: 10 y: 6',
                ' x: 0 y: 4',
                ' x: 1 y: 4',
                ' x: 2 y: 4',
                ' x: 3 y: 4',
                ' x: 4 y: 4',
                ' x: 5 y: 4',
                ' x: 6 y: 4',
                ' x: 7 y: 4',
                ' x: 8 y: 4',
                ' x: 9 y: 4',
                ' x: 10 y: 4',
                ' x: 0 y: 7',
                ' x: 1 y: 7',
                ' x: 2 y: 7',
                ' x: 3 y: 7',
                ' x: 4 y: 7',
                ' x: 5 y: 7',
                ' x: 6 y: 7',
                ' x: 7 y: 7',
                ' x: 8 y: 7',
                ' x: 9 y: 7',
                ' x: 10 y: 7',
                ' x: 0 y: 3',
                ' x: 1 y: 3',
                ' x: 2 y: 3',
                ' x: 3 y: 3',
                ' x: 4 y: 3',
                ' x: 5 y: 3',
                ' x: 6 y: 3',
                ' x: 7 y: 3',
                ' x: 8 y: 3',
                ' x: 9 y: 3',
                ' x: 10 y: 3',
                ' x: 3 y: 10',
                ' x: 3 y: 0',
                ' x: 4 y: 10',
                ' x: 4 y: 0',
                ' x: 5 y: 10',
                ' x: 5 y: 0',
                ' x: 6 y: 10',
                ' x: 6 y: 0',
                ' x: 7 y: 10',
                ' x: 7 y: 0',
                ' x: 1 y: 8',
                ' x: 2 y: 8',
                ' x: 3 y: 8',
                ' x: 4 y: 8',
                ' x: 5 y: 8',
                ' x: 6 y: 8',
                ' x: 7 y: 8',
                ' x: 8 y: 8',
                ' x: 9 y: 8',
                ' x: 1 y: 2',
                ' x: 2 y: 2',
                ' x: 3 y: 2',
                ' x: 4 y: 2',
                ' x: 5 y: 2',
                ' x: 6 y: 2',
                ' x: 7 y: 2',
                ' x: 8 y: 2',
                ' x: 9 y: 2',
                ' x: 2 y: 9',
                ' x: 2 y: 1',
                ' x: 3 y: 9',
                ' x: 3 y: 1',
                ' x: 4 y: 9',
                ' x: 4 y: 1',
                ' x: 5 y: 9',
                ' x: 5 y: 1',
                ' x: 6 y: 9',
                ' x: 6 y: 1',
                ' x: 7 y: 9',
                ' x: 7 y: 1',
                ' x: 8 y: 9',
                ' x: 8 y: 1']
    for i in range(len(circle)):
        assert(str(circle[i] == result[i]))
    print('OK')

def position_properties():
    print('Test: position_properties')
    pos_1 = Position(x=1, y=2, angle=4)
    pos_2 = Position(x=1, y=2, angle=4)
    pos_3 = Position(x=1, angle=4, z=5, y=2)
    assert(str(pos_1) == ' x: 1 y: 2 angle: 4')
    assert(str(pos_2) == ' x: 1 y: 2 angle: 4')
    assert(str(pos_3) == ' x: 1 y: 2 z: 5 angle: 4')
    assert(pos_1 == pos_2)
    assert(pos_1 != pos_3)
    assert(pos_2 != pos_3)
    poses = set([])
    assert(len(poses) == 0)
    poses.add(pos_1)
    assert(len(poses) == 1)
    poses.add(pos_3)
    assert(len(poses) == 2)
    poses.add(pos_2)
    assert(len(poses) == 2)
    print('OK')

if __name__ == '__main__':
    map_to_grid_pos()
    map_to_real_pos()
    utils_bresenham_line()
    utils_filled_midpoint_circle()
    position_properties()
    print('End of tests')
    print('OK')
