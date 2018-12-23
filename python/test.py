from mapping.map import Map
from utils.position import Position

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

if __name__ == '__main__':
    map_to_grid_pos()
    map_to_real_pos()
    print('End of tests')
    print('OK')
